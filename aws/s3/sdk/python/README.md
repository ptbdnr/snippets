
# S3 Sync

Requirements:
- Python 3.6+
- AWS CLI installed
- AWS credentials configured (e.g., via `aws configure`)


```shell
python3 -m venv .venv && source .venv/bin/activate
pip install awscli
pip install -r requirements.txt
```

verify that AWS credentials are configured correctly:
```shell
aws sts get-caller-identity
# This should return the AWS account ID and ARN of the IAM user or role
# If you see an error, make sure your AWS credentials are set up correctly.
aws configure
```


```shell
# Sync local directory to S3 bucket
python s3_sync.py /local/path s3://bucket-name/prefix

# Sync from S3 bucket to local directory
python s3_sync.py s3://bucket-name/prefix /local/path

# Sync with deletion (remove files in destination that don't exist in source)
python s3_sync.py /local/path s3://bucket-name/prefix --delete

# Perform a dry run to see what would happen
python s3_sync.py /local/path s3://bucket-name/prefix --dryrun

# Exclude certain files/directories
python s3_sync.py /local/path s3://bucket-name/prefix --exclude "*.log" --exclude ".git/*"
```