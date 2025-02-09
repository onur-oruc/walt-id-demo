import os
import requests
import dotenv

dotenv.load_dotenv()

WALLET_API_URL = os.getenv("WALLET_API_URL")


def create_key(did: str):
    url = f"{WALLET_API_URL}/v1/key"
    headers = {"Content-Type": "application/json"}
    data = {"did": did}
    response = requests.post(url, headers=headers, json=data)
    return response.json()
