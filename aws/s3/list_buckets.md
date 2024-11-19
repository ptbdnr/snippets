# Python SDK

This section uses your local computer.
For AWS, Python SDK is Boto3: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

## Workspace setup
install python3.10: https://www.python.org/downloads/release/python-3100/

Create a new folder on your local computer.

Create an environment 

on Unix:
```bash
python3.10 -m venv .venv
source .venv/bin/activate
```
on Windows
```batch
python3.10 -m venv .venv
.venv/Scripts/activate.bat
```

install boto3
```bash
pip install --upgrade pip
pip install boto3
```

## Use the SDK

run the following to list the S3 buckets
```bash
python3.10 -c "import boto3; [print(b['Name']) for b in boto3.client('s3').list_buckets()['Buckets']]"
```

Troubleshooting
1. Error: botocore.exceptions.SSLError: SSL validation failed for. As a workaround for this session try
```bash
python3.10 -c "import boto3; [print(b['Name']) for b in boto3.client('s3', verify=False).list_buckets()['Buckets']]"
```