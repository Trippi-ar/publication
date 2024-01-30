import requests
import json

from app.config import settings


def authenticate(token: str, role_request: str):
    url = Settings.AUTH_URL
    payload = json.dumps({
        "token": token,
        "role_request": role_request
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.status_code)
