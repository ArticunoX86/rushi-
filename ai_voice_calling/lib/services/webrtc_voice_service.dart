import 'dart:async';
import 'package:dio/dio.dart';
import 'package:livekit_client/livekit_client.dart';
import '../core/config/app_config.dart';
import '../core/logger/app_logger.dart';
import '../core/network/dio_client.dart';

class WebRTCVoiceService {
  WebRTCVoiceService._internal();
  static final WebRTCVoiceService instance = WebRTCVoiceService._internal();

  Room? _room;
  bool _isConnected = false;
  bool get isConnected => _isConnected;

  final Dio _dio = DioClient.instance.dio;

  /// Requests a WebRTC room token from the backend for the given callId
  Future<Map<String, String>?> _fetchWebRTCToken(String callId) async {
    try {
      final url = '${AppConfig.baseUrl}/webrtc/token';
      AppLogger.logger.i('Requesting WebRTC Token: $url for callId: $callId');

      final response = await _dio.post(
        url,
        data: {
          'call_id': callId,
          'identity': 'mobile_client_${DateTime.now().millisecondsSinceEpoch}',
        },
      );

      if (response.statusCode == 200 && response.data != null) {
        final data = response.data;
        return {
          'token': data['token'] as String,
          'room_name': data['room_name'] as String,
        };
      }
    } catch (e) {
      AppLogger.logger.e('Failed to fetch WebRTC Token', e);
    }
    return null;
  }

  /// Connects to the WebRTC LiveKit Room for real-time audio streaming
  Future<bool> startVoiceSession(String callId, {String? livekitUrl}) async {
    try {
      AppLogger.logger.i('Starting WebRTC Voice Session for callId: $callId');

      final tokenData = await _fetchWebRTCToken(callId);
      if (tokenData == null) {
        AppLogger.logger.e('Cannot start WebRTC session: Token fetch failed');
        return false;
      }

      final token = tokenData['token']!;
      final url = livekitUrl ?? AppConfig.websocketUrl;

      _room = Room();

      // Setup Event Listeners
      _room!.events.listen((event) {
        if (event is TrackSubscribedEvent) {
          AppLogger.logger.i('🟢 WebRTC Track Subscribed: ${event.track.sid}');
        } else if (event is RoomDisconnectedEvent) {
          AppLogger.logger.i('🔴 WebRTC Room Disconnected');
          _isConnected = false;
        }
      });

      // Connect to LiveKit WebRTC Room
      await _room!.connect(
        url,
        token,
        roomOptions: const RoomOptions(
          defaultAudioPublishOptions: AudioPublishOptions(
            audioBitrate: 32000,
            dtx: true,
          ),
        ),
      );

      // Publish local microphone audio track over WebRTC
      await _room!.localParticipant?.setMicrophoneEnabled(true);
      _isConnected = true;

      AppLogger.logger.i('🚀 WebRTC Voice Session Established & Microphone Streaming Active!');
      return true;
    } catch (e) {
      AppLogger.logger.e('Error in WebRTC Voice Session', e);
      _isConnected = false;
      return false;
    }
  }

  /// Disconnects and releases WebRTC resources
  Future<void> stopVoiceSession() async {
    try {
      if (_room != null) {
        AppLogger.logger.i('Stopping WebRTC Voice Session...');
        await _room!.disconnect();
        await _room!.dispose();
        _room = null;
      }
      _isConnected = false;
      AppLogger.logger.i('WebRTC Voice Session Stopped.');
    } catch (e) {
      AppLogger.logger.e('Error stopping WebRTC Voice Session', e);
    }
  }
}
