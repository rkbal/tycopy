import requests
import json

# CONFIGURATION
BASE_URL = 'https://your-thycotic-url/SecretServer'
API_URL = f'{BASE_URL}/api/v1'
USERNAME = 'your-username'
PASSWORD = 'your-password'
DOMAIN = ''  # Leave blank if not using AD
AUTH_URL = f'{BASE_URL}/oauth2/token'

# TLS SECRET TEMPLATE ID (use /secret-templates to find your org's)
TLS_TEMPLATE_ID = 12345  # Example; adjust based on your setup
TLS_FOLDER_ID = 2  # Change to your preferred folder

# Step 1: Get Auth Token
def get_token():
    data = {
        'username': USERNAME,
        'password': PASSWORD,
        'grant_type': 'password',
        'domain': DOMAIN
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(AUTH_URL, data=data, headers=headers)
    response.raise_for_status()
    return response.json()['access_token']

# Step 2: Create TLS Secret
def create_tls_secret(token, name, cert_pem, private_key, key_password=''):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # You must use correct item IDs for cert, key, etc. from your template
    payload = {
        "name": name,
        "folderId": TLS_FOLDER_ID,
        "secretTemplateId": TLS_TEMPLATE_ID,
        "items": [
            {"itemId": 1, "itemValue": cert_pem},        # e.g., Certificate
            {"itemId": 2, "itemValue": private_key},     # e.g., Private Key
            {"itemId": 3, "itemValue": key_password}     # Optional Password
        ]
    }

    response = requests.post(f'{API_URL}/secrets', headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

# Step 3: Upload TLS Secret
if __name__ == '__main__':
    cert_path = 'my-cert.pem'
    key_path = 'my-key.pem'

    with open(cert_path, 'r') as cert_file:
        cert_content = cert_file.read()

    with open(key_path, 'r') as key_file:
        key_content = key_file.read()

    token = get_token()
    secret = create_tls_secret(token, 'My TLS Cert Secret', cert_content, key_content)
    print("✅ TLS Secret Created:")
    print(json.dumps(secret, indent=2))
