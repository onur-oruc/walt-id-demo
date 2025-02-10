import os
import requests
from datetime import datetime, timedelta
import uuid
import json
from fastapi import status


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
        issuance_date = datetime.utcnow().isoformat() + "Z"
        expiration_date = (datetime.utcnow() + timedelta(days=365)).isoformat() + "Z"

        # Create selective disclosure fields
        sd_fields = {}
        for field in selective_disclosure_fields:
            sd_fields[field] = {"sd": True}

        body = {
            "issuerKey": issuer_key,
            "credentialConfigurationId": "OpenBadgeCredential_jwt_vc_json",
            "credentialData": {
                "@context": [
                    "https://www.w3.org/2018/credentials/v1",
                    "https://purl.imsglobal.org/spec/ob/v3p0/context.json",
                ],
                "id": f"urn:uuid:{credential_id}",
                "type": ["VerifiableCredential", "OpenBadgeCredential"],
                "issuer": credential_data["issuer"],
                "credentialSubject": credential_data["credentialSubject"],
            },
            "selectiveDisclosure": {
                "fields": sd_fields,
                "decoyMode": "NONE",
                "decoys": 0,
            },
            "mapping": {
                "id": credential_id,
                "issuer": {"id": issuer_did},
                "credentialSubject": {"id": subject_did},
                "issuanceDate": issuance_date,
                "expirationDate": expiration_date,
            },
            "authenticationMethod": "PRE_AUTHORIZED",
            "issuerDid": issuer_did,
            "standardVersion": "DRAFT13",
        }

        # Ensure proper JSON formatting with double quotes
        body_json = json.dumps(body, ensure_ascii=False, separators=(",", ":"))

        response = requests.post(url, json=json.loads(body_json), headers=headers)
        print(f"VC issuance response status: {response.status_code}")
        print(f"VC issuance response content: {response.text}")

        if response.status_code != status.HTTP_200_OK:
            return None

        result = {
            "credential": response.text,
            "credential_id": credential_id,
        }
        return result

