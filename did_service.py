import os
import requests
import dotenv

dotenv.load_dotenv()

WALLET_API_URL = os.getenv("WALLET_API_URL")


def create_did(did: str):
    url = f"{WALLET_API_URL}/v1/did"
    headers = {"Content-Type": "application/json"}
    data = {"did": did}
    response = requests.post(url, headers=headers, json=data)
    return response.json()


def generate_did_document(did: str): ...
