package com.aivoicecalling.ai_voice_calling

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.os.IBinder
import android.telephony.TelephonyCallback
import android.telephony.TelephonyManager
import android.util.Log
import androidx.core.app.NotificationCompat

class CallService : Service() {

    companion object {
        private const val TAG = "CallService"
        private const val CHANNEL_ID = "CallServiceChannel"
        private const val NOTIFICATION_ID = 8888

        interface CallStateListener {
            fun onCallStateChanged(state: String)
        }

        var listener: CallStateListener? = null
        private var activeState: String = "IDLE"

        fun updateState(state: String) {
            activeState = state
            listener?.onCallStateChanged(state)
        }

        fun getActiveState(): String {
            return activeState
        }
    }

    private lateinit var telephonyManager: TelephonyManager
    private var callback: TelephonyCallback? = null

    override fun onCreate() {
        super.onCreate()
        Log.d(TAG, "CallService onCreate")
        createNotificationChannel()
        startTelephonyListener()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        Log.d(TAG, "CallService onStartCommand")
        val phoneNumber = intent?.getStringExtra("phoneNumber")

        // Build starting notification
        val notification = createNotification("AI Sales Call", "Initiating call...")
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            startForeground(
                NOTIFICATION_ID,
                notification,
                android.content.pm.ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC
            )
        } else {
            startForeground(NOTIFICATION_ID, notification)
        }

        if (!phoneNumber.isNullOrEmpty()) {
            try {
                val callIntent = Intent(Intent.ACTION_CALL).apply {
                    data = Uri.parse("tel:$phoneNumber")
                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }
                startActivity(callIntent)
            } catch (e: Exception) {
                Log.e(TAG, "Failed to start phone call: ${e.message}")
                updateState("FAILED")
            }
        }

        return START_STICKY
    }

    private fun startTelephonyListener() {
        telephonyManager = getSystemService(Context.TELEPHONY_SERVICE) as TelephonyManager
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            callback = object : TelephonyCallback(), TelephonyCallback.CallStateListener {
                override fun onCallStateChanged(state: Int) {
                    handleCallState(state)
                }
            }
            try {
                telephonyManager.registerTelephonyCallback(mainExecutor, callback!!)
                Log.d(TAG, "TelephonyCallback registered in Service")
            } catch (e: SecurityException) {
                Log.e(TAG, "SecurityException registering TelephonyCallback: ${e.message}")
            }
        }
    }

    private var isInitialCallState = true

    private fun handleCallState(state: Int) {
        val stateStr = when (state) {
            TelephonyManager.CALL_STATE_IDLE -> "IDLE"
            TelephonyManager.CALL_STATE_RINGING -> "RINGING"
            TelephonyManager.CALL_STATE_OFFHOOK -> "OFFHOOK"
            else -> "UNKNOWN"
        }
        Log.d(TAG, "CallState changed in Service: $stateStr")

        if (isInitialCallState && stateStr == "IDLE") {
            isInitialCallState = false
            Log.d(TAG, "Ignoring initial IDLE state")
            return
        }
        isInitialCallState = false

        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        val detail = when (stateStr) {
            "IDLE" -> "Call ended"
            "RINGING" -> "Ringing..."
            "OFFHOOK" -> "Call active"
            else -> "Service running"
        }
        
        val notification = createNotification("AI Sales Call", detail)
        notificationManager.notify(NOTIFICATION_ID, notification)

        updateState(stateStr)

        if (stateStr == "IDLE") {
            stopSelf()
        }
    }

    private fun createNotification(title: String, content: String): Notification {
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle(title)
            .setContentText(content)
            .setSmallIcon(android.R.drawable.sym_call_outgoing)
            .setOngoing(true)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val serviceChannel = NotificationChannel(
                CHANNEL_ID,
                "Call Service Channel",
                NotificationManager.IMPORTANCE_LOW
            )
            val manager = getSystemService(NotificationManager::class.java)
            manager?.createNotificationChannel(serviceChannel)
        }
    }

    override fun onDestroy() {
        Log.d(TAG, "CallService onDestroy")
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S && callback != null) {
            telephonyManager.unregisterTelephonyCallback(callback!!)
        }
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? {
        return null
    }
}
