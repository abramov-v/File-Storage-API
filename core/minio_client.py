import boto3
import botocore

from core.config import (
                    MINIO_ENDPOINT,
                    MINIO_ACCESS_KEY,
                    MINIO_SECRET_KEY,
                    MINIO_BUCKET
                    )


minio_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY
)


def create_bucket():
    try:
        minio_client.head_bucket(Bucket=MINIO_BUCKET)
    except Exception:
        minio_client.create_bucket(Bucket=MINIO_BUCKET)


create_bucket()


def get_presigned_url(file_key: str, expiration: int = 3600):
    try:
        url = minio_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': MINIO_BUCKET, 'Key': file_key},
            ExpiresIn=expiration
        )
        return url
    except botocore.exceptions.ClientError as e:
        print(f'Error generating presigned URL: {e}')
        return None


def delete_file_from_minio(file_key: str):
    try:
        minio_client.delete_object(Bucket=MINIO_BUCKET, Key=file_key)
        print(f'Successfully deleted file: {file_key}')
        return True
    except botocore.exceptions.ClientError as e:
        print(f'Error deleting file: {e}')
        return False
