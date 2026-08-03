package com.aivoicecalling.ai_voice_calling

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.util.Log
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.EventChannel
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {

    companion object {
        private const val CHANNEL = "ai_voice_calling/phone"
        private const val EVENT_CHANNEL = "ai_voice_calling/call_state"
        private const val REALTIME_CHANNEL = "ai_voice_calling/realtime_audio"
        private const val REQUEST_CALL_PERMISSION = 1001
    }

    private val realTimeAudioService by lazy { RealTimeAudioService(this) }

    private var pendingPhoneNumber: String? = null

    override fun configureFlutterEngine(
        flutterEngine: FlutterEngine
    ) {
        super.configureFlutterEngine(flutterEngine)

        registerVoipPhoneAccount()

        // =====================================================
        // EVENT CHANNEL (Android -> Flutter)
        // =====================================================

        EventChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            EVENT_CHANNEL
        ).setStreamHandler(
            CallStateStreamHandler(this)
        )

        // =====================================================
        // METHOD CHANNEL (Flutter -> Android)
        // =====================================================

        MethodChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            CHANNEL
        ).setMethodCallHandler { call, result ->

            when (call.method) {

                "makeCall" -> {

                    val phoneNumber =
                        call.argument<String>("phoneNumber")

                    if (phoneNumber.isNullOrEmpty()) {

                        result.error(
                            "INVALID_NUMBER",
                            "Phone number is empty.",
                            null
                        )

                        return@setMethodCallHandler
                    }

                    makePhoneCall(phoneNumber)

                    result.success(true)
                }

                else -> result.notImplemented()
            }
        }

        // =====================================================
        // REALTIME AUDIO CHANNEL (Flutter -> Android)
        // =====================================================

        val realtimeChannel = MethodChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            REALTIME_CHANNEL
        )

        realTimeAudioService.listener = object : RealTimeAudioService.AudioServiceListener {
            override fun onLog(level: String, message: String) {
                runOnUiThread {
                    realtimeChannel.invokeMethod(
                        "onNativeLog",
                        mapOf("level" to level, "message" to message)
                    )
                }
            }
        }

        realtimeChannel.setMethodCallHandler { call, result ->
            when (call.method) {
                "startStreaming" -> {
                    val callId = call.argument<String>("callId") ?: ""
                    val wsUrl = call.argument<String>("wsUrl") ?: ""
                    realTimeAudioService.startStreaming(callId, wsUrl)
                    result.success(true)
                }
                "stopStreaming" -> {
                    realTimeAudioService.stopStreaming()
                    result.success(true)
                }
                else -> result.notImplemented()
            }
        }
    }

    private fun makePhoneCall(
        phoneNumber: String
    ) {

        val hasCallPermission =
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.CALL_PHONE
            ) == PackageManager.PERMISSION_GRANTED

        val hasPhoneStatePermission =
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.READ_PHONE_STATE
            ) == PackageManager.PERMISSION_GRANTED

        val hasRecordAudioPermission =
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.RECORD_AUDIO
            ) == PackageManager.PERMISSION_GRANTED

        val hasNotificationPermission = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.POST_NOTIFICATIONS
            ) == PackageManager.PERMISSION_GRANTED
        } else {
            true
        }

        val requiredPermissions = mutableListOf(
            Manifest.permission.CALL_PHONE,
            Manifest.permission.READ_PHONE_STATE,
            Manifest.permission.RECORD_AUDIO
        )
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            requiredPermissions.add(Manifest.permission.POST_NOTIFICATIONS)
        }

        if (!hasCallPermission || !hasPhoneStatePermission || !hasNotificationPermission || !hasRecordAudioPermission) {

            pendingPhoneNumber = phoneNumber

            ActivityCompat.requestPermissions(
                this,
                requiredPermissions.toTypedArray(),
                REQUEST_CALL_PERMISSION
            )

            return
        }

        val serviceIntent = Intent(this, CallService::class.java).apply {
            putExtra("phoneNumber", phoneNumber)
        }
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            startForegroundService(serviceIntent)
        } else {
            startService(serviceIntent)
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {

        super.onRequestPermissionsResult(
            requestCode,
            permissions,
            grantResults
        )

        if (requestCode == REQUEST_CALL_PERMISSION) {
            val callGranted = ContextCompat.checkSelfPermission(this, Manifest.permission.CALL_PHONE) == PackageManager.PERMISSION_GRANTED
            val stateGranted = ContextCompat.checkSelfPermission(this, Manifest.permission.READ_PHONE_STATE) == PackageManager.PERMISSION_GRANTED
            val audioGranted = ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED

            if (callGranted && stateGranted && audioGranted) {
                Log.d(
                    "PERMISSION",
                    "Essential permissions granted."
                )

                pendingPhoneNumber?.let {
                    makePhoneCall(it)
                }

            } else {

                Log.e(
                    "PERMISSION",
                    "Required permissions denied."
                )
            }
        }
    }

    private fun registerVoipPhoneAccount() {
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            try {
                val telecomManager = getSystemService(Context.TELECOM_SERVICE) as android.telecom.TelecomManager
                val componentName = android.content.ComponentName(this, VoipConnectionService::class.java)
                val phoneAccountHandle = android.telecom.PhoneAccountHandle(componentName, "AI_VOICE_ACCOUNT")

                val phoneAccount = android.telecom.PhoneAccount.builder(phoneAccountHandle, "AI Voice Gateway")
                    .setCapabilities(android.telecom.PhoneAccount.CAPABILITY_SELF_MANAGED or android.telecom.PhoneAccount.CAPABILITY_CALL_PROVIDER)
                    .build()

                telecomManager.registerPhoneAccount(phoneAccount)
                Log.d("Telecom", "Registered Voip PhoneAccount successfully")
            } catch (e: Exception) {
                Log.e("Telecom", "Failed to register Voip PhoneAccount: ${e.message}")
            }
        }
    }
}