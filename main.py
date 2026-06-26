import os
import time
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Read environment variables
access_key_id = os.environ.get("iam_access_key_user_key_id")
secret_access_key = os.environ.get("iam_access_key_user_key_secret")
bucket_name = os.environ.get("bucket_name")

# Validate all required env vars are set
missing = [
    name for name, val in [
        ("iam_access_key_user_key_id", access_key_id),
        ("iam_access_key_user_key_secret", secret_access_key),
        ("bucket_name", bucket_name),
    ]
    if not val
]

if missing:
    raise EnvironmentError(f"Missing required environment variable(s): {', '.join(missing)}")

print(f"Connecting to S3 bucket: {bucket_name}")

# Create S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
)

# Check connection by heading the bucket
try:
    s3.head_bucket(Bucket=bucket_name)
    print(f"Successfully connected to bucket '{bucket_name}'.")
except ClientError as e:
    error_code = e.response["Error"]["Code"]
    if error_code == "404":
        raise RuntimeError(f"Bucket '{bucket_name}' does not exist.") from e
    elif error_code in ("401", "403"):
        raise RuntimeError(f"Access denied to bucket '{bucket_name}'. Check your credentials.") from e
    else:
        raise RuntimeError(f"Failed to connect to bucket '{bucket_name}': {e}") from e
except NoCredentialsError as e:
    raise RuntimeError("Invalid or missing AWS credentials.") from e

print("S3 connection check passed. Sleeping indefinitely...")

while True:
    time.sleep(3600)