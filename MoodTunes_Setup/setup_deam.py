import boto3
import os
from botocore.exceptions import NoCredentialsError
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# Load AWS credentials from environment variables
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = 'deam-dataset-private'
PREFIX = 'DEAM/'
LOCAL_DIR = Path("DEAM")

def download_from_s3(bucket, prefix, local_dir):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY)
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if key.endswith('/'):
                continue
            relative_path = key[len(prefix):]
            local_path = local_dir / relative_path
            local_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"⬇ Downloading {key} to {local_path}")
            s3.download_file(bucket, key, str(local_path))

if __name__ == '__main__':
    LOCAL_DIR.mkdir(exist_ok=True)
    try:
        download_from_s3(BUCKET_NAME, PREFIX, LOCAL_DIR)
        print("✅ Download complete!")
    except NoCredentialsError:
        print("❌ AWS credentials not found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.")
