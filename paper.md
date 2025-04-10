---
title: 'Manage mTLS secrets (certificates/keys) in Thycotic Secret Server using a Python script.'
tags:
  - Python
  - thycotic

authors:
  - name: Rajat Kumar Bal
date: 10 April 2025

---

# Summary

Manage TLS secrets (certificates/keys) in Thycotic Secret Server using a Python script. 


# Statement of need

Automate the retrieval, renewal, or rotation of mTLS certificates stored in **Thycotic Secret Server**, using Python scripts via the **REST API**, integrated into a **Jenkins pipeline**.


# Prerequisites:
- Thycotic Secret Server (TSS) REST API enabled
- A secret containing the mTLS certificate (e.g., .pfx or PEM parts)
- API access credentials (client ID/secret or username/password)
- Python 3 environment
- Jenkins with Python installed or Docker image
- Permissions to access secrets

# 1. Authenticate to Thycotic REST API

Use the OAuth2 client credentials flow (or password flow if enabled).

Python Code (OAuth2 client credentials):
```python
import requests

def get_access_token(base_url, client_id, client_secret):
    token_url = f"{base_url}/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "secrets"
    }
    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    return response.json()['access_token']
```


# 2. Retrieve Secret Containing mTLS Certificate

If you have the secret ID or name, fetch it like this:

```python
def get_secret(base_url, access_token, secret_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    secret_url = f"{base_url}/api/v1/secrets/{secret_id}"
    response = requests.get(secret_url, headers=headers)
    response.raise_for_status()
    return response.json()
```

For certs, your secret likely has fields like:
- `Certificate` (PEM)
- `PrivateKey` (PEM)
- `PFX` (Base64)
- `Password` (if needed for import)


# 3. Use the Certificate (e.g., Deploy or Renew)

You could:
- Decode and save the cert to disk
- Use `OpenSSL` or a Python library (like `cryptography`) to inspect or renew it
- Use `requests` with `cert=(cert.pem, key.pem)` for mTLS client requests

Example to decode and write the cert:

```python
import base64

def save_cert_to_file(cert_b64, filename):
    cert_bytes = base64.b64decode(cert_b64)
    with open(filename, "wb") as f:
        f.write(cert_bytes)
```



# 4. Jenkins Integration

In Jenkins:
- Store your Thycotic credentials as secrets or use a credentials plugin
- Use a `Python` build step or run a `sh` script calling your Python automation
- Securely pass secrets/environment variables

Jenkinsfile Example
```groovy
pipeline {
    agent any
    environment {
        TSS_CLIENT_ID = credentials('thycotic-client-id')
        TSS_CLIENT_SECRET = credentials('thycotic-client-secret')
    }
    stages {
        stage('Retrieve mTLS Cert') {
            steps {
                sh 'python3 scripts/get_certificate.py'
            }
        }
        stage('Deploy Cert') {
            steps {
                sh './deploy_certificate.sh' // e.g., restart service using the cert
            }
        }
    }
}
```



# Acknowledgements

We acknowledge contributions from Rajat Kumar Bal during the CA state healthcare project.

# References
Most od them confidential  to CA state health care project
