from deepgram import (
    DeepgramClient,
    LiveOptions,
    LiveTranscriptionEvents,
)


from app.core.config import settings



# ==================================================
# DEEPGRAM REALTIME STREAMING CLIENT
# ==================================================

class DeepgramLiveClient:


    def __init__(self, on_transcript=None):


        self.client = DeepgramClient(

            settings.DEEPGRAM_API_KEY

        )


        self.connection = None

        self.on_transcript = on_transcript


        # sends transcript to AI orchestrator
        self.transcript_callback = None





    # ==================================================
    # START STREAM
    # ==================================================

    async def start(self):


        self.connection = (

            self.client.listen.asyncwebsocket.v("1")

        )




        # ==============================================
        # RECEIVE TRANSCRIPTS FROM DEEPGRAM
        # ==============================================

        async def on_message(

            self_connection,

            result,

            **kwargs,

        ):


            try:


                transcript = (

                    result.channel
                    .alternatives[0]
                    .transcript

                )


                is_final = result.is_final




                if transcript:


                    print(

                        "\n================================"

                    )


                    print(

                        "CUSTOMER SAID:",

                        transcript

                    )


                    print(

                        "FINAL:",

                        is_final

                    )


                    print(

                        "================================\n"

                    )




                    # =================================
                    # SEND TEXT TO AI BRAIN
                    # =================================

                    if self.on_transcript:


                        await self.on_transcript(

                            transcript,

                            is_final

                        )






            except Exception as e:


                print(

                    "TRANSCRIPT ERROR:",

                    e

                )





        # ==============================================
        # REGISTER EVENT LISTENERS
        # ==============================================

        async def on_open(self_connection, open, **kwargs):
            print("DEEPGRAM CONNECTION OPENED")

        async def on_close(self_connection, close, **kwargs):
            print("DEEPGRAM CONNECTION CLOSED")

        async def on_error(self_connection, error, **kwargs):
            print("DEEPGRAM ERROR:", error)

        async def on_metadata(self_connection, metadata, **kwargs):
            print("DEEPGRAM METADATA:", metadata)

        self.connection.on(
            LiveTranscriptionEvents.Open,
            on_open,
        )

        self.connection.on(
            LiveTranscriptionEvents.Close,
            on_close,
        )

        self.connection.on(
            LiveTranscriptionEvents.Error,
            on_error,
        )

        self.connection.on(
            LiveTranscriptionEvents.Metadata,
            on_metadata,
        )

        self.connection.on(

            LiveTranscriptionEvents.Transcript,

            on_message,

        )






        # ==============================================
        # DEEPGRAM CONFIG
        # ==============================================

        options = LiveOptions(

            model="nova-2",

            language="en-US",

            encoding="linear16",

            sample_rate=16000,

            channels=1,

            smart_format=True,

            interim_results=True,

            endpointing=1000,

            vad_events=True,

        )





        await self.connection.start(

            options

        )




        print(

            "Deepgram Live Connected"

        )









    # ==================================================
    # SEND AUDIO CHUNKS
    # ==================================================

    async def send_audio(

        self,

        audio: bytes,

    ):


        if self.connection:


            await self.connection.send(

                audio

            )








    # ==================================================
    # CLOSE CONNECTION
    # ==================================================

    async def close(self):


        if self.connection:


            await self.connection.finish()



            print(

                "Deepgram Closed"

            )