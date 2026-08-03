package com.aivoicecalling.ai_voice_calling

import android.content.Context
import android.util.Log
import io.flutter.plugin.common.EventChannel

class CallStateStreamHandler(
    private val context: Context
) : EventChannel.StreamHandler {

    companion object {
        private const val TAG = "CALL_STATE"
    }

    private var eventSink: EventChannel.EventSink? = null

    override fun onListen(
        arguments: Any?,
        events: EventChannel.EventSink?
    ) {
        Log.d(TAG, "onListen() called")
        eventSink = events

        // Send current active state immediately
        eventSink?.success(CallService.getActiveState())

        // Register for updates from the service
        CallService.listener = object : CallService.Companion.CallStateListener {
            override fun onCallStateChanged(state: String) {
                android.os.Handler(android.os.Looper.getMainLooper()).post {
                    eventSink?.success(state)
                }
            }
        }
    }

    override fun onCancel(arguments: Any?) {
        Log.d(TAG, "onCancel()")
        CallService.listener = null
        eventSink = null
    }
}