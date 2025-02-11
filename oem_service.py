import os
import uuid
import requests
import json
import hashlib
from fastapi import status
from datetime import datetime, timezone
from vc_issuer import VCIssuer


class OEMService:
    def __init__(self):
        self.issuer_api = os.getenv("ISSUER_API_URL")
        self.wallet_api = os.getenv("WALLET_API_URL")
        self.wallet_id = os.getenv("OEM_WALLET_ID")
        self.oem_domain = os.getenv("OEM_DOMAIN")
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
            "domain": f"{self.oem_domain}",
            "path": f"/oem/battery/{serial_number}",
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

    def create_initial_battery_vc(self, battery_did, serial_number, token):
        # Load OEM issuer credentials
        # first we need to get the issuer did by serial number
        if not battery_did:
            return {"status": "error", "message": "Battery DID not found"}

        try:
            with open("oem_issuer_credentials.json", "r") as f:
                issuer_creds = json.load(f)
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to load issuer credentials: {str(e)}",
            }

        # Prepare credential data
        credential_data = {
            "issuer": {
                "type": ["Battery OEM"],
                "name": f"Initial Battery VC for {serial_number}",
                "url": "https://www.jff.org/",
                "image": "https://w3c-ccg.github.io/vc-ed/plugfest-1-2022/images/JFF_LogoLockup.png",
            },
            # "credentialSubject": {
            #     "id": battery_did,
            #     "type": "Battery",
            #     "serialNumber": serial_number,
            #     "manufacturer": "OEM",
            #     "manufacturingDate": datetime.utcnow().isoformat() + "Z",
            #     "initialHealth": 100,
            #     "warrantyStatus": "active",
            #     "technicalDetails": {
            #         "capacity": "5000mAh",
            #         "chemistry": "Li-ion",
            #         "voltage": "3.7V",
            #         "maxChargeCurrent": "2A",
            #         "maxDischargeCurrent": "3A",
            #         "operatingTemperature": "-20°C to 60°C",
            #     },
            #     "qualityControl": {
            #         "testResults": "PASSED",
            #         "inspector": "QC-123",
            #         "testDate": datetime.utcnow().isoformat() + "Z",
            #         "testBatch": "B2024-001",
            #     },
            # },
            "credentialSubject": {
                "type": ["BatterySubject"],
                "initialData": {
                    "id": f"urn:uuid:{uuid.uuid4()}",
                    "type": ["Genesis"],
                    "name": f"Initial Battery VC for {serial_number}",
                    "description": "This is the initial battery VC for the battery with serial number {serial_number}",
                    "qualityControl": {
                        "testResults": "PASSED",
                        "inspector": "QC-123",
                        "testDate": datetime.now(timezone.utc).isoformat() + "Z",
                        "testBatch": "B2024-001",
                    },
                    "technicalDetails": {
                        "capacity": "5000mAh",
                        "chemistry": "Li-ion",
                        "voltage": "3.7V",
                        "maxChargeCurrent": "2A",
                        "maxDischargeCurrent": "3A",
                        "operatingTemperature": "-20°C to 60°C",
                    },
                    "image": {
                        "id": "https://w3c-ccg.github.io/vc-ed/plugfest-3-2023/images/JFF-VC-EDU-PLUGFEST3-badge-image.png",
                        "type": "Image",
                    },
                },
            },
        }

        # Fields to be selectively disclosed
        selective_disclosure_fields = [
            "credentialSubject.technicalDetails",
            "credentialSubject.qualityControl",
            "credentialSubject.initialHealth",
            "credentialSubject.warrantyStatus",
        ]

        # Issue the VC using SD-JWT
        vc_issuer = VCIssuer()
        result = vc_issuer.issue_sd_jwt_vc(
            issuer_key=issuer_creds["issuerKey"],
            issuer_did=issuer_creds["issuerDid"],
            subject_did=battery_did,
            credential_data=credential_data,
            selective_disclosure_fields=selective_disclosure_fields,
            token=token,
        )

        if result:
            return {
                "status": "success",
                "message": "Battery VC created with selective disclosure",
                "vc_offer": result,
            }
        else:
            return {"status": "error", "message": "Failed to create battery VC"}

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

    def get_all_wallet_dids(self, token):
        url = f"{self.wallet_api}/wallet-api/wallet/{self.wallet_id}/dids"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        return response.json()

    def get_all_wallet_credentials(self, token):
        url = f"{self.wallet_api}/wallet-api/wallet/{self.wallet_id}/credentials"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        return response.json()

    def get_battery_did_by_serial_number(self, serial_number, token):
        all_dids = self.get_all_wallet_dids(token)
        for did in all_dids:
            if did["did"].split(":")[-1] == serial_number:
                return did["did"]
        return None
