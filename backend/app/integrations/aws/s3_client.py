import boto3
from datetime import datetime
from app.core.config import settings

# ==================================================
# AWS S3 CLIENT
# ==================================================
s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)

# ==================================================
# UPLOAD AUDIO FILE
# ==================================================
def upload_audio_file(
    audio_bytes: bytes,
    call_id: str,
    extension: str = "wav",
    content_type: str = "audio/wav",
):
    timestamp = datetime.utcnow().strftime(
        "%Y%m%d_%H%M%S"
    )
    filename = (
        f"calls/{call_id}_{timestamp}.{extension}"
    )

    s3_client.put_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=filename,
        Body=audio_bytes,
        ContentType=content_type,
    )

    audio_url = (
        f"https://{settings.S3_BUCKET_NAME}"
        f".s3.{settings.AWS_REGION}"
        f".amazonaws.com/{filename}"
    )

    print(
        "Uploaded to S3:",
        audio_url
    )

    return audio_url

# ==================================================
# CREATE TEMP DOWNLOAD LINK
# ==================================================
def generate_presigned_url(
    filename: str,
    expiry: int = 3600,
):
    return s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.S3_BUCKET_NAME,
            "Key": filename,
        },
        ExpiresIn=expiry,
    )