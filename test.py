from base64 import b64encode
from dotenv import load_dotenv
import json, os, requests
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

def encode_credentials():
    base_string = f'{CLIENT_ID}:{CLIENT_SECRET}'
    base_bytes = base_string.encode('ascii')
    encode_string = b64encode(base_bytes)
    return encode_string.decode('ascii')

def save_tokens(t1, t2):
    with open('.env', 'r') as file:
        data = file.readlines()
    data[2] = f'ACCESS_TOKEN={t1}\n'
    data[3] = f'REFRESH_TOKEN={t2}\n'

    with open('.env', 'w') as file:
        file.writelines(data)

def get_new_tokens():
    url = 'https://api.fitbit.com/oauth2/token'
    
    client_key = encode_credentials()
    auth_header = f'Basic {client_key}'

    headers = {
        'Authorization': auth_header,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN
    }

    r = requests.post(url, data=payload, headers = headers)

    json_response = r.json()
    if 'errors' in json_response:
        print('Could not connect.')
        for e in json_response['errors']:
            error_type = e['errorType']
            error_message = e['message']
            print(f'Error Type: {error_type}, Message: {error_message}')
    else:
        t1 = json_response['access_token']
        t2 = json_response['refresh_token']
        print(t1)
        print(t2)
        save_tokens(t1,t2)

def is_token_valid():
    url = 'https://api.fitbit.com/1.1/oauth2/introspect'

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {'token': f'{ACCESS_TOKEN}'}

    r = requests.post(url, data=data, headers=headers).json()
    
    return r['active']

if __name__ == '__main__':
    if is_token_valid():
        print('Token is valid')
    else:
        get_new_tokens()

    