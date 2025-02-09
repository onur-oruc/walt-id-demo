import os
import sys
import dotenv

dotenv.load_dotenv()

ISSUER_API_URL = os.getenv("ISSUER_API_URL")
WALLET_API_URL = os.getenv("WALLET_API_URL")
VERIFIER_API_URL = os.getenv("VERIFIER_API_URL")

print(ISSUER_API_URL)
print(WALLET_API_URL)
print(VERIFIER_API_URL)


"""
todo: 
- Register (we need 4 accounts -- OEM, 2 repairers, auditor)§ one of the repairers will not have the permission to issue credential for the battery
- Create DIDs (OEM, repairer, auditor, battery)
- Login 
- Issue Credential (OEM should be able to issue credential to repairer and auditor)
    - OEM should be able to issue credential to repairer and auditor
    - Repairer should be able to issue credential to the battery
- Verify Credential (auditor should be able to verify the credential(s) issued by OEM and repairer)
- Get Credential (repairer should be able to get the credential)
- Get Credential Status (auditor should be able to get the status of the credential)
- Get Credential Revocation List (auditor should be able to get the revocation list)
- Get Credential Revocation List Status (auditor should be able to get the status of the revocation list)
"""
