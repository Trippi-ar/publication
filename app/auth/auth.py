import requests
import json


def authenticate(token: str, role_request: str):
    url = "http://users_ms:8000/api/users/auth"

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
        print(data)
        return data
    else:
        print(response.status_code)
