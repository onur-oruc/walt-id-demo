import os
import requests
import json
import hashlib
from fastapi import status
from datetime import datetime


class OEMService:
    def __init__(self):
        self.issuer_api = os.getenv("ISSUER_API_URL")
        self.wallet_api = os.getenv("WALLET_API_URL")
        self.wallet_id = os.getenv("OEM_WALLET_ID")
        self.oem_did = None

    def create_jwk_key(self, token: str) -> str:
        """
        Create a JWK key in the wallet
        Returns the key id if the key is created successfully
        """
        url = f"{self.wallet_api}/wallet-api/wallet/{self.wallet_id}/keys/generate"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        data = {"backend": "jwk", "keyType": "Ed25519"}

        response = requests.post(url, json=data, headers=headers)
        print(f"Key creation response status: {response.status_code}")
        print(f"Key creation response content: {response.text}")

        return response.text

    def create_battery_did(self, serial_number, token):
        # First create a key
        key = self.create_jwk_key(token)
        if not key:
            return {"status": "error", "message": "Failed to create key for DID"}

        # Then create DID using query parameters
        params = {
            "domain": f"battery-{serial_number}.oem.com",
            "path": f"/battery/{serial_number}",
            "keyId": key,
            "alias": f"battery-{serial_number}",
        }

        url = f"{self.wallet_api}/wallet-api/wallet/{self.wallet_id}/dids/create/web"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        response = requests.post(url, params=params, headers=headers)

        print(f"DID creation response status: {response.status_code}")
        print(f"DID creation response content: {response.text}")

        if response.status_code == status.HTTP_200_OK:
            return {
                "status": "success",
                "message": "DID created",
                "did": response.text,
            }
        elif response.status_code == 400:
            return {"status": "error", "message": "DID could not be created"}
        elif response.status_code == 401:
            return {"status": "error", "message": "Invalid authentication"}
        elif response.status_code == 409:
            return {"status": "error", "message": "DID already exists"}
        else:
            return {
                "status": "error",
                "message": f"Unknown error: {response.status_code}",
            }

    def create_initial_battery_vc(self, battery_did, serial_number):
        credential = {
            "@context": [
                "https://www.w3.org/2018/credentials/v1",
                "https://w3id.org/security/suites/jws-2020/v1",
            ],
            "type": ["VerifiableCredential", "BatteryCredential"],
            "issuer": self.oem_did,
            "issuanceDate": datetime.utcnow().isoformat() + "Z",
            "credentialSubject": {
                "id": battery_did,
                "type": "Battery",
                "serialNumber": serial_number,
                "manufacturer": "OEM",
                "manufacturingDate": datetime.utcnow().isoformat() + "Z",
                "initialHealth": 100,
                "warrantyStatus": "active",
            },
        }

        response = requests.post(
            f"{self.issuer_api}/credentials/issue", json={"credential": credential}
        )
        return response.json()

    def create_hash_of_battery_vc(self, battery_vc):
        vc_string = json.dumps(battery_vc, sort_keys=True)
        return hashlib.sha256(vc_string.encode()).hexdigest()

    def create_oem_issuer_did_web(self, token):
        url = f"{self.issuer_api}/onboard/issuer"
        body = {
            "key": {"backend": "jwk", "keyType": "secp256k1"},
            "did": {
                "method": "web",
                "config": {"domain": "oem.com", "path": "/oem"},
            },
        }

        response = requests.post(url, json=body)
        return response.json()
