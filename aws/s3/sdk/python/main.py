import logging
from pathlib import Path

import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PROFILE = "****"
S3_BUCKET_NAME = "****"
S3_TARGET_BUCKET_NAME = "****"
REGION = "eu-west-1"

PREFIX = "****"
KEY = "****"
DOWNLOAD_DIR = "download"

session = boto3.session.Session(profile_name=PROFILE)
s3 = boto3.client("s3", REGION)
s3_resource = boto3.resource("s3", REGION)

# Get object storage class
s3_object = s3_resource.Object(S3_BUCKET_NAME, KEY)
logger.info(s3_object.storage_class)

# Download by key
s3.download_file(Bucket=S3_BUCKET_NAME, Key=KEY, Filename=str(Path(DOWNLOAD_DIR) / KEY))

# Download by prefix
paginator = s3.get_paginator("list_objects_v2")
pages = paginator.paginate(Bucket=S3_BUCKET_NAME, Prefix=PREFIX)
for page in pages:
    for obj in page["Contents"]:
        data = (obj["Key"], obj["Key"].split("/")[-1], obj["Size"])
        logger.info(data)
        s3.download_file(Bucket=S3_BUCKET_NAME, Key=data[0], Filename=str(Path(DOWNLOAD_DIR) / PREFIX / data[1]))

# Restore from Glacier by key
response = s3.restore_object(
    Bucket=S3_BUCKET_NAME,
    Key=KEY,
    RestoreRequest={
        "Days": 21,
        "GlacierJobParameters": {"Tier": "Bulk"},
})

# Copy object
s3.copy_object(
    Bucket=S3_TARGET_BUCKET_NAME,
    Key=KEY,
    CopySource={"Bucket": S3_BUCKET_NAME, "Key": KEY}
)

# Delete object
s3.delete_object(Bucket=S3_BUCKET_NAME, Key=KEY)
