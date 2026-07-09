import sounddevice as sd
import numpy as np


# ==================================================
# MIC TEST
# ==================================================

def callback(
    indata,
    frames,
    time,
    status,
):

    volume = np.linalg.norm(
        indata
    )


    print(
        "MIC LEVEL:",
        volume
    )



with sd.InputStream(

    samplerate=16000,

    channels=1,

    dtype="int16",

    callback=callback,

):


    input(
        "Speak now. Press ENTER to stop\n"
    )