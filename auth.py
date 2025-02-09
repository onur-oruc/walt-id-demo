import os
import requests
import dotenv

dotenv.load_dotenv()

WALLET_API_URL = os.getenv("WALLET_API_URL")


def login(did: str, key: str):
    url = f"{WALLET_API_URL}/v1/login"
    headers = {"Content-Type": "application/json"}
    data = {"did": did, "key": key}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def login_with_email(email: str, password: str):
    url = f"{WALLET_API_URL}/wallet-api/auth/login"
    headers = {"Content-Type": "application/json"}
    data = {"email": email, "password": password, "type": "email"}
    response = requests.post(url, headers=headers, json=data)
    return response.json()
