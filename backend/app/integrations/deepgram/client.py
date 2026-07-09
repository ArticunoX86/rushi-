import requests


from app.core.config import settings



# ==================================================
# SPEECH TO TEXT
# ==================================================

def speech_to_text(
    audio_url: str,
):


    try:


        url = (
            "https://api.deepgram.com/v1/listen"
        )


        headers = {

            "Authorization": (
                f"Token {settings.DEEPGRAM_API_KEY}"
            ),

            "Content-Type": "application/json",

        }


        params = {

            "model": "nova-3",

            "smart_format": "true",

            "detect_language": "true",

            "punctuate": "true",

        }


        payload = {

            "url": audio_url

        }



        response = requests.post(

            url,

            headers=headers,

            params=params,

            json=payload,

        )



        data = response.json()


        print(
            "DEEPGRAM RESPONSE:",
            data
        )



        transcript = (
            data["results"]
            ["channels"]
            [0]
            ["alternatives"]
            [0]
            ["transcript"]
        )


        return transcript




    except Exception as e:


        print(
            "=============================="
        )

        print(
            "Deepgram Error:",
            e
        )

        print(
            "=============================="
        )


        return None