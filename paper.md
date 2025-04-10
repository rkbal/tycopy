---
title: 'manage TLS secrets (certificates/keys) in Thycotic Secret Server using a Python script.'
tags:
  - Python
  - thycotic

authors:
  - name: Rajat Kumar Bal
date: 10 April 2025

---

# Summary

Manage TLS secrets (certificates/keys) in Thycotic Secret Server using a Python script. 
That’s totally doable using the Thycotic REST API — especially if your org stores 
certificates (TLS secrets) using the built-in SSL Certificate secret template (or a custom one).


# Statement of need

manage mTLS certificates in Thycotic Secret Server using Python, Thycotic REST API, and 
Jenkins, here's a high-level plan with some starter code to help you automate this workflow.

Automate the retrieval, renewal, or rotation of mTLS certificates stored in Thycotic Secret 
Server, using Python scripts via the REST API, integrated into a Jenkins pipeline.


# Prerequisites

Prerequisites:
Thycotic Secret Server (TSS) REST API enabled
A secret containing the mTLS certificate (e.g., .pfx or PEM parts)
API access credentials (client ID/secret or username/password)
Python 3 environment
Jenkins with Python installed or Docker image
Permissions to access secrets

# Acknowledgements

We acknowledge contributions from Rajat Kumar Bal during the CA state healthcare project.

# References
Most od them confidential  to CA state health care project
