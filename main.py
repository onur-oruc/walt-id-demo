import os
import requests
import dotenv
from oem_service import OEMService

dotenv.load_dotenv()

ISSUER_API_URL = os.getenv("ISSUER_API_URL")
WALLET_API_URL = os.getenv("WALLET_API_URL")
VERIFIER_API_URL = os.getenv("VERIFIER_API_URL")
OEM_WALLET_ID = os.getenv("OEM_WALLET_ID")
API_URL = os.getenv("API_URL", "http://localhost:8000")

# print("Environment variables:")
# print(f"ISSUER_API_URL: {ISSUER_API_URL}")
# print(f"WALLET_API_URL: {WALLET_API_URL}")
# print(f"VERIFIER_API_URL: {VERIFIER_API_URL}")
# print(f"OEM_WALLET_ID: {OEM_WALLET_ID}")

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


def get_token(username: str, password: str):
    response = requests.post(
        f"{API_URL}/token", data={"username": username, "password": password}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("Authentication failed")


def main():
    try:
        # Get authentication token
        print("Getting authentication token...")
        token = get_token("oem_user", "oem_password")  # Replace with actual credentials

        # Initialize OEM service
        oem = OEMService()

        # Create battery DID
        print("\nCreating Battery DID...")
        serial_number = "BAT123456"
        result = oem.create_battery_did(serial_number, token)

        if result["status"] == "success":
            print(f"Success: {result['message']}")
            print(f"DID: {result['did']}")
            battery_did = result["did"]
        else:
            print(f"Error: {result['message']}")
            return

    except Exception as e:
        print(f"Error in main: {e}")


if __name__ == "__main__":
    main()
