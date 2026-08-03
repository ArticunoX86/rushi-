package com.aivoicecalling.ai_voice_calling

import android.Manifest
import android.content.pm.PackageManager
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaRecorder
import android.util.Log
import androidx.core.content.ContextCompat
import okhttp3.*
import okio.ByteString
import okio.ByteString.Companion.toByteString
import java.util.concurrent.TimeUnit

class RealTimeAudioService(
    private val context: android.content.Context
) {
    interface AudioServiceListener {
        fun onLog(level: String, message: String)
    }

    var listener: AudioServiceListener? = null

    companion object {
        private const val TAG = "RealTimeAudioService"
        private const val SAMPLE_RATE = 16000
        private const val CHANNEL_CONFIG = AudioFormat.CHANNEL_IN_MONO
        private const val AUDIO_FORMAT = AudioFormat.ENCODING_PCM_16BIT
        private const val CHUNK_SIZE = 4096
    }

    private var audioRecord: AudioRecord? = null
    private var isStreaming = false
    private var streamingThread: Thread? = null
    private var webSocket: WebSocket? = null
    private var mediaPlayer: android.media.MediaPlayer? = null
    private val audioManager by lazy {
        context.getSystemService(android.content.Context.AUDIO_SERVICE) as android.media.AudioManager
    }
    private val client = OkHttpClient.Builder()
        .readTimeout(0, TimeUnit.MILLISECONDS)
        .build()

    // ==================================================
    private fun playAudioBytes(bytes: ByteArray) {
        try {
            val voipConn = VoipConnectionService.activeConnection
            if (voipConn != null) {
                Log.d(TAG, "Streaming ${bytes.size} audio bytes directly to Telecom VoipConnection")
                voipConn.playAudioTrack(bytes)
                return
            }

            mediaPlayer?.stop()
            mediaPlayer?.release()
            mediaPlayer = null

            val tempFile = java.io.File.createTempFile("ai_voice", ".mp3", context.cacheDir)
            tempFile.deleteOnExit()
            java.io.FileOutputStream(tempFile).use { fos ->
                fos.write(bytes)
            }

            try {
                audioManager.mode = android.media.AudioManager.MODE_IN_COMMUNICATION
                audioManager.isSpeakerphoneOn = false
            } catch (e: Exception) {
                Log.e(TAG, "Error setting in-call mode: ${e.message}")
            }

            val audioAttributes = android.media.AudioAttributes.Builder()
                .setUsage(android.media.AudioAttributes.USAGE_VOICE_COMMUNICATION)
                .setContentType(android.media.AudioAttributes.CONTENT_TYPE_SPEECH)
                .build()

            mediaPlayer = android.media.MediaPlayer().apply {
                setAudioAttributes(audioAttributes)
                setDataSource(tempFile.absolutePath)
                prepare()
                start()
            }
            Log.d(TAG, "Playing AI voice audio: ${bytes.size} bytes on USAGE_VOICE_COMMUNICATION")
        } catch (e: Exception) {
            Log.e(TAG, "Error playing audio bytes: ${e.message}")
        }
    }

    // ==================================================
    // START STREAMING
    // ==================================================

    fun startStreaming(callId: String, wsUrl: String) {
        if (isStreaming) {
            val msg = "Already streaming — ignoring startStreaming()"
            Log.w(TAG, msg)
            listener?.onLog("WARN", msg)
            return
        }

        val hasAudioPermission = ContextCompat.checkSelfPermission(
            context,
            Manifest.permission.RECORD_AUDIO
        ) == PackageManager.PERMISSION_GRANTED

        if (!hasAudioPermission) {
            val errMsg = "RECORD_AUDIO permission not granted!"
            Log.e(TAG, errMsg)
            listener?.onLog("ERROR", errMsg)
            return
        }

        var baseUrl = wsUrl
        if (baseUrl.endsWith("/")) {
            baseUrl = baseUrl.substring(0, baseUrl.length - 1)
        }
        val fullUrl = "$baseUrl/realtime/call/$callId"
        val connectMsg = "Connecting realtime WebSocket: $fullUrl"
        Log.d(TAG, connectMsg)
        listener?.onLog("INFO", connectMsg)

        val request = Request.Builder().url(fullUrl).build()

        webSocket = client.newWebSocket(request, object : WebSocketListener() {

            override fun onOpen(webSocket: WebSocket, response: Response) {
                val openMsg = "Realtime WebSocket opened — starting mic capture"
                Log.d(TAG, openMsg)
                listener?.onLog("INFO", openMsg)
                startMicCapture()
            }

            override fun onMessage(webSocket: WebSocket, text: String) {
                Log.d(TAG, "Realtime message (text): $text")
            }

            override fun onMessage(webSocket: WebSocket, bytes: ByteString) {
                if (!isStreaming) {
                    val warnMsg = "Discarded ${bytes.size} audio bytes received before call went OFFHOOK"
                    Log.w(TAG, warnMsg)
                    listener?.onLog("WARN", warnMsg)
                    return
                }
                Log.d(TAG, "Realtime message (audio): ${bytes.size} bytes")
                playAudioBytes(bytes.toByteArray())
            }

            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                val errMsg = "Realtime WebSocket failure: ${t.message}"
                Log.e(TAG, errMsg)
                listener?.onLog("ERROR", errMsg)
                stopMicCapture()
            }

            override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                val closeMsg = "Realtime WebSocket closed: $reason"
                Log.d(TAG, closeMsg)
                listener?.onLog("INFO", closeMsg)
                stopMicCapture()
            }
        })
    }

    // ==================================================
    // STOP STREAMING
    // ==================================================

    fun stopStreaming() {
        Log.d(TAG, "stopStreaming() called")
        stopMicCapture()
        webSocket?.close(1000, "Call ended")
        webSocket = null

        try {
            mediaPlayer?.stop()
            mediaPlayer?.release()
            mediaPlayer = null
        } catch (e: Exception) {
            Log.e(TAG, "Error releasing media player: ${e.message}")
        }
    }

    // ==================================================
    // MICROPHONE CAPTURE LOOP
    // ==================================================

    private fun startMicCapture() {
        try {
            audioManager.mode = android.media.AudioManager.MODE_IN_COMMUNICATION
            audioManager.isSpeakerphoneOn = false
            Log.d(TAG, "AudioManager mode set to MODE_IN_COMMUNICATION")
        } catch (e: Exception) {
            Log.e(TAG, "Error setting AudioManager mode: ${e.message}")
        }

        val minBufferSize = AudioRecord.getMinBufferSize(
            SAMPLE_RATE,
            CHANNEL_CONFIG,
            AUDIO_FORMAT
        )
        val bufferSize = maxOf(minBufferSize, CHUNK_SIZE * 4)

        audioRecord = AudioRecord(
            MediaRecorder.AudioSource.VOICE_COMMUNICATION,
            SAMPLE_RATE,
            CHANNEL_CONFIG,
            AUDIO_FORMAT,
            bufferSize
        )

        if (audioRecord?.state != AudioRecord.STATE_INITIALIZED) {
            Log.e(TAG, "AudioRecord failed to initialize")
            return
        }

        isStreaming = true
        audioRecord?.startRecording()
        Log.d(TAG, "Mic recording started @ ${SAMPLE_RATE}Hz")

        streamingThread = Thread {
            val buffer = ByteArray(CHUNK_SIZE)
            while (isStreaming) {
                val read = audioRecord?.read(buffer, 0, CHUNK_SIZE) ?: -1
                if (read > 0 && webSocket != null) {
                    val chunk = buffer.copyOf(read)
                    webSocket?.send(chunk.toByteString())
                }
            }
            Log.d(TAG, "Mic capture loop exited")
        }.also { it.start() }
    }

    private fun stopMicCapture() {
        isStreaming = false
        streamingThread?.join(2000)
        streamingThread = null
        audioRecord?.stop()
        audioRecord?.release()
        audioRecord = null

        try {
            audioManager.mode = android.media.AudioManager.MODE_NORMAL
            Log.d(TAG, "AudioManager mode reset to MODE_NORMAL")
        } catch (e: Exception) {
            Log.e(TAG, "Error resetting AudioManager mode: ${e.message}")
        }

        Log.d(TAG, "Mic capture stopped and released")
    }
}
