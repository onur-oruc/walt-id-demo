import os
import requests
import json
import hashlib
from datetime import datetime


class OEMService:
    def __init__(self):
        self.issuer_api = os.getenv("ISSUER_API_URL")
        self.wallet_api = os.getenv("WALLET_API_URL")
        self.wallet_id = os.getenv("OEM_WALLET_ID")
        self.oem_did = None

    def create_battery_did(self, serial_number, token):
        url = f"{self.wallet_api}/wallet-api/wallet/{self.wallet_id}/dids/create/web"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        data = {
            "domain": f"battery-{serial_number}.example.com",
            "path": f"/battery/{serial_number}",
            "keyId": f"battery-key-{serial_number}",
            "alias": f"battery-{serial_number}",
        }

        response = requests.post(url, json=data, headers=headers)

        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")

        if response.status_code == 200:
            response_data = response.json()
            return {
                "status": "success",
                "message": "DID created",
                "did": response_data.get("content", {}).get("did"),
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
