import os
import requests
from datetime import datetime, timedelta
import uuid


class VCIssuer:
    def __init__(self):
        self.issuer_api = os.getenv("ISSUER_API_URL")

    def issue_sd_jwt_vc(
        self,
        issuer_key: dict,
        issuer_did: str,
        subject_did: str,
        credential_data: dict,
        selective_disclosure_fields: list,
        token: str,
    ):
        """
        Issues a Verifiable Credential using SD-JWT format
        """
        url = f"{self.issuer_api}/openid4vc/sdjwt/issue"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        # Generate unique ID for the credential
        credential_id = str(uuid.uuid4())
        issuance_date = datetime.utcnow()
        expiration_date = issuance_date + timedelta(days=365)

        body = {
            "issuerKey": issuer_key,
            "credentialConfigurationId": "BatteryCredential_jwt_vc_json",
            "credentialData": {
                "@context": [
                    "https://www.w3.org/2018/credentials/v1",
                    "https://w3id.org/security/suites/jws-2020/v1",
                ],
                "id": f"urn:uuid:{credential_id}",
                "type": ["VerifiableCredential", "BatteryCredential"],
                **credential_data,
            },
            "mapping": {
                "id": "<uuid>",
                "issuer": {"id": "<issuerDid>"},
                "credentialSubject": {"id": "<subjectDid>"},
                "issuanceDate": "<timestamp>",
                "expirationDate": "<timestamp-in:365d>",
            },
            "selectiveDisclosure": {
                "fields": {
                    field: {"sd": True} for field in selective_disclosure_fields
                },
                "decoyMode": "NONE",
                "decoys": 0,
            },
            "authenticationMethod": "PRE_AUTHORIZED",
            "issuerDid": issuer_did,
            "standardVersion": "DRAFT13",
        }

        response = requests.post(url, json=body, headers=headers)
        print(f"VC issuance response status: {response.status_code}")
        print(f"VC issuance response content: {response.text}")

        return response.json() if response.status_code == 200 else None
