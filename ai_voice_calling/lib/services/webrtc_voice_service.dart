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
      final url = '${AppConfig.apiBaseUrl}/webrtc/token';
      AppLogger.info('Requesting WebRTC Token: $url for callId: $callId');

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
      AppLogger.error('Failed to fetch WebRTC Token', error: e);
    }
    return null;
  }

  /// Connects to the WebRTC LiveKit Room for real-time audio streaming
  Future<bool> startVoiceSession(String callId, {String? livekitUrl}) async {
    try {
      AppLogger.info('Starting WebRTC Voice Session for callId: $callId');

      final tokenData = await _fetchWebRTCToken(callId);
      if (tokenData == null) {
        AppLogger.error('Cannot start WebRTC session: Token fetch failed');
        return false;
      }

      final token = tokenData['token']!;
      final url = livekitUrl ?? AppConfig.wsBaseUrl.replaceAll('ws://', 'ws://').replaceAll('wss://', 'wss://');

      _room = Room();

      // Setup Event Listeners
      _room!.events.listen((event) {
        if (event is TrackSubscribedEvent) {
          AppLogger.info('🟢 WebRTC Track Subscribed: ${event.track.sid}');
        } else if (event is RoomDisconnectedEvent) {
          AppLogger.info('🔴 WebRTC Room Disconnected');
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

      AppLogger.info('🚀 WebRTC Voice Session Established & Microphone Streaming Active!');
      return true;
    } catch (e) {
      AppLogger.error('Error in WebRTC Voice Session', error: e);
      _isConnected = false;
      return false;
    }
  }

  /// Disconnects and releases WebRTC resources
  Future<void> stopVoiceSession() async {
    try {
      if (_room != null) {
        AppLogger.info('Stopping WebRTC Voice Session...');
        await _room!.disconnect();
        await _room!.dispose();
        _room = null;
      }
      _isConnected = false;
      AppLogger.info('WebRTC Voice Session Stopped.');
    } catch (e) {
      AppLogger.error('Error stopping WebRTC Voice Session', error: e);
    }
  }
}
