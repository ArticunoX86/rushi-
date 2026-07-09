from app.integrations.aws.s3_client import (
    upload_audio_file,
)



print(
    "Starting AWS S3 Upload Test..."
)



# ==================================================
# TEST AUDIO DATA
# ==================================================

audio_bytes = b"This is my AI call recording test"



print(
    "Audio Size:",
    len(audio_bytes),
    "bytes"
)





# ==================================================
# UPLOAD
# ==================================================

url = upload_audio_file(

    audio_bytes,

    "test_call_001"

)





print(
    "=============================="
)

print(
    "UPLOAD SUCCESS"
)

print(
    "S3 URL:"
)

print(
    url
)

print(
    "=============================="
)