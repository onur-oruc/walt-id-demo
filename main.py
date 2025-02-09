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

"""
required functions:
create_hash_of_battery_vc()
find_latest_battery_vc(): by timestamp
create_permission_vc(): oem creates permission vc for repairer
create_initial_battery_vc(): oem creates initial battery vc for battery

oem:
- create_hash_of_battery_vc()
- find_latest_battery_vc()
- create_permission_vc()
- create_initial_battery_vc()
- revoke_permission_vc()
- revoke_battery_vc()

repairer:
- create_hash_of_battery_vc()
- find_latest_battery_vc()
- create_permission_vc()


system verification:
- verify_repairer_has_permission(): checks if repairer has permission to issue credential for the battery


verifier:
- list_chain_of_battery_changes(given_battery): lists all the battery changes (VCs)
- list_permission_vc(given_battery): lists all the permission VCs

    cursor suggestions:
    - display_revocation_status(): lists all the revocation statuses (VCs)
    - display_credential_status(): lists all the credential statuses (VCs)
    - display_credential_revocation_list(): lists all the credential revocation lists (VCs)
    - display_credential_revocation_list_status(): lists all the credential revocation list statuses (VCs)



"""
