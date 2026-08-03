import 'dart:async';
import 'package:flutter/services.dart';
import '../core/config/app_config.dart';
import '../core/logger/app_logger.dart';

/// Flutter-side bridge to the native [RealTimeAudioService] in Kotlin.
/// Starts/stops mic streaming to the backend /realtime/call/{callId} WebSocket.
class RealTimeAudioService {
  RealTimeAudioService._() {
    _channel.setMethodCallHandler((call) async {
      if (call.method == 'onNativeLog') {
        final args = call.arguments as Map;
        final level = args['level'] as String;
        final message = args['message'] as String;
        if (level == 'ERROR') {
          AppLogger.logger.e('Native: $message');
        } else if (level == 'WARN') {
          AppLogger.logger.w('Native: $message');
        } else {
          AppLogger.logger.i('Native: $message');
        }
      }
    });
  }

  static final RealTimeAudioService instance = RealTimeAudioService._();

  static const MethodChannel _channel =
      MethodChannel('ai_voice_calling/realtime_audio');

  String? _activeCallId;

  // ==================================================
  // REGISTER CALL ID (called before OFFHOOK fires)
  // ==================================================

  void registerCallId(String callId) {
    _activeCallId = callId;
    AppLogger.logger.i('🎙️ Registered callId for streaming: $callId');
  }

  // ==================================================
  // START STREAMING
  // ==================================================

  Future<void> startStreaming(String callId) async {
    _activeCallId = callId;
    final wsUrl = AppConfig.websocketUrl;

    AppLogger.logger.i('🎙️ Starting realtime audio stream for call: $callId');

    try {
      await _channel.invokeMethod('startStreaming', {
        'callId': callId,
        'wsUrl': wsUrl,
      });
      AppLogger.logger.i('🎙️ Realtime audio stream started');
    } on PlatformException catch (e) {
      AppLogger.logger.e('Failed to start realtime audio', error: e);
    }
  }

  // ==================================================
  // STOP STREAMING
  // ==================================================

  Future<void> stopStreaming() async {
    if (_activeCallId == null) return;

    AppLogger.logger.i('🛑 Stopping realtime audio stream');

    try {
      await _channel.invokeMethod('stopStreaming');
      AppLogger.logger.i('🛑 Realtime audio stream stopped');
    } on PlatformException catch (e) {
      AppLogger.logger.e('Failed to stop realtime audio', error: e);
    } finally {
      _activeCallId = null;
    }
  }

  String? get activeCallId => _activeCallId;
}
