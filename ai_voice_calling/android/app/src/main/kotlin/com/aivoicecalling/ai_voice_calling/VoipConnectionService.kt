package com.aivoicecalling.ai_voice_calling

import android.telecom.Connection
import android.telecom.ConnectionRequest
import android.telecom.ConnectionService
import android.telecom.PhoneAccountHandle
import android.util.Log

class VoipConnectionService : ConnectionService() {

    companion object {
        private const val TAG = "VoipConnectionService"
        var activeConnection: VoipConnection? = null
    }

    override fun onCreateOutgoingConnection(
        connectionManagerPhoneAccount: PhoneAccountHandle?,
        request: ConnectionRequest?
    ): Connection {
        Log.d(TAG, "onCreateOutgoingConnection: ${request?.address}")
        val connection = VoipConnection()
        connection.setAddress(request?.address, android.telecom.TelecomManager.PRESENTATION_ALLOWED)
        connection.setDialing()
        connection.setActive()
        activeConnection = connection
        CallService.updateState("OFFHOOK")
        return connection
    }

    override fun onCreateIncomingConnection(
        connectionManagerPhoneAccount: PhoneAccountHandle?,
        request: ConnectionRequest?
    ): Connection {
        Log.d(TAG, "onCreateIncomingConnection: ${request?.address}")
        val connection = VoipConnection()
        connection.setAddress(request?.address, android.telecom.TelecomManager.PRESENTATION_ALLOWED)
        connection.setRinging()
        activeConnection = connection
        CallService.updateState("RINGING")
        return connection
    }

    override fun onCreateOutgoingConnectionFailed(
        connectionManagerPhoneAccount: PhoneAccountHandle?,
        request: ConnectionRequest?
    ) {
        Log.e(TAG, "onCreateOutgoingConnectionFailed")
        CallService.updateState("FAILED")
    }

    override fun onCreateIncomingConnectionFailed(
        connectionManagerPhoneAccount: PhoneAccountHandle?,
        request: ConnectionRequest?
    ) {
        Log.e(TAG, "onCreateIncomingConnectionFailed")
        CallService.updateState("FAILED")
    }
}
