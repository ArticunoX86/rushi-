package com.aivoicecalling.ai_voice_calling

import android.media.AudioAttributes
import android.media.AudioFormat
import android.media.AudioTrack
import android.os.Build
import android.telecom.CallAudioState
import android.telecom.Connection
import android.telecom.DisconnectCause
import android.util.Log

class VoipConnection : Connection() {

    companion object {
        private const val TAG = "VoipConnection"
        private const val SAMPLE_RATE = 16000
    }

    private var audioTrack: AudioTrack? = null
    private var isPlaying = false

    init {
        connectionCapabilities = CAPABILITY_SUPPORT_HOLD or CAPABILITY_HOLD
        audioModeIsVoip = true
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            connectionProperties = PROPERTY_SELF_MANAGED
        }
    }

    override fun onShowIncomingCallUi() {
        Log.d(TAG, "onShowIncomingCallUi()")
        setActive()
    }

    override fun onAnswer() {
        Log.d(TAG, "onAnswer()")
        setActive()
        CallService.updateState("OFFHOOK")
    }

    override fun onReject() {
        Log.d(TAG, "onReject()")
        setDisconnected(DisconnectCause(DisconnectCause.REJECTED))
        destroy()
        CallService.updateState("IDLE")
    }

    override fun onDisconnect() {
        Log.d(TAG, "onDisconnect()")
        stopAudioPlayback()
        setDisconnected(DisconnectCause(DisconnectCause.LOCAL))
        destroy()
        CallService.updateState("IDLE")
    }

    override fun onAbort() {
        Log.d(TAG, "onAbort()")
        stopAudioPlayback()
        setDisconnected(DisconnectCause(DisconnectCause.CANCELED))
        destroy()
        CallService.updateState("IDLE")
    }

    override fun onCallAudioStateChanged(state: CallAudioState?) {
        Log.d(TAG, "onCallAudioStateChanged: $state")
    }

    fun playAudioTrack(pcmBytes: ByteArray) {
        try {
            if (audioTrack == null) {
                val minBufferSize = AudioTrack.getMinBufferSize(
                    SAMPLE_RATE,
                    AudioFormat.CHANNEL_OUT_MONO,
                    AudioFormat.ENCODING_PCM_16BIT
                )
                val audioAttributes = AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_VOICE_COMMUNICATION)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                    .build()

                val audioFormat = AudioFormat.Builder()
                    .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                    .setSampleRate(SAMPLE_RATE)
                    .setChannelMask(AudioFormat.CHANNEL_OUT_MONO)
                    .build()

                audioTrack = AudioTrack.Builder()
                    .setAudioAttributes(audioAttributes)
                    .setAudioFormat(audioFormat)
                    .setBufferSizeInBytes(maxOf(minBufferSize, pcmBytes.size))
                    .setTransferMode(AudioTrack.MODE_STREAM)
                    .build()

                audioTrack?.play()
                isPlaying = true
            }

            audioTrack?.write(pcmBytes, 0, pcmBytes.size)
        } catch (e: Exception) {
            Log.e(TAG, "Error in playAudioTrack: ${e.message}")
        }
    }

    private fun stopAudioPlayback() {
        try {
            isPlaying = false
            audioTrack?.stop()
            audioTrack?.release()
            audioTrack = null
        } catch (e: Exception) {
            Log.e(TAG, "Error stopping audio track: ${e.message}")
        }
    }
}
