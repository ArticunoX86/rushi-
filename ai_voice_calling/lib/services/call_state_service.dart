import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import '../core/logger/app_logger.dart';
import '../features/calls/services/call_action_service.dart';
import 'realtime_audio_service.dart';

class CallStateService {
  CallStateService._();

  static final CallStateService instance =
      CallStateService._();

  static const EventChannel _eventChannel =
      EventChannel(
    "ai_voice_calling/call_state",
  );

  StreamSubscription? _subscription;
  bool _hasCallStarted = false;

  void startListening() {
    debugPrint("=================================");
    debugPrint("CALL STATE SERVICE STARTED");
    debugPrint("=================================");

    _subscription ??=
        _eventChannel.receiveBroadcastStream().listen(
      (event) {
        AppLogger.logger.i("📞 CALL STATE : $event");
        if (event == "OFFHOOK" || event == "RINGING") {
           _hasCallStarted = true;
           // Start streaming mic audio to AI backend when call is active
           if (event == "OFFHOOK") {
             final callId = RealTimeAudioService.instance.activeCallId;
             if (callId != null) {
               RealTimeAudioService.instance.startStreaming(callId);
             } else {
               AppLogger.logger.w('⚠️ OFFHOOK but no activeCallId set — skip streaming');
             }
           }
        }
        if (event == "IDLE") {
           if (_hasCallStarted) {
             CallActionService.instance.endCall();
             RealTimeAudioService.instance.stopStreaming();
             _hasCallStarted = false;
           }
        }
      },
      onError: (error) {
        AppLogger.logger.e("❌ CALL STATE ERROR : $error");
      },
      onDone: () {
        AppLogger.logger.w("⚠️ CALL STATE STREAM CLOSED");
      },
    );
  }

  Future<void> stopListening() async {
    await _subscription?.cancel();
    _subscription = null;
  }
}