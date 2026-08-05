import 'dart:async';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:livekit_client/livekit_client.dart';
import 'package:dio/dio.dart';

import '../../../core/config/app_config.dart';
import '../../../core/logger/app_logger.dart';

final livekitListenProvider =
    StateNotifierProvider<LiveKitListenNotifier, ListenState>((ref) {
  return LiveKitListenNotifier();
});

class ListenState {
  final bool isListening;
  final bool isLoading;
  final String? error;

  ListenState({
    this.isListening = false,
    this.isLoading = false,
    this.error,
  });

  ListenState copyWith({bool? isListening, bool? isLoading, String? error}) {
    return ListenState(
      isListening: isListening ?? this.isListening,
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }
}

class LiveKitListenNotifier extends StateNotifier<ListenState> {
  LiveKitListenNotifier() : super(ListenState());

  Room? _room;
  final Dio _dio = Dio();

  EventsListener<RoomEvent>? _listener;

  Future<void> startListening(String callId) async {
    if (state.isListening || state.isLoading) return;

    state = state.copyWith(isLoading: true, error: null);

    try {
      // 1. Fetch token
      final response = await _dio.get(
        '${AppConfig.baseUrl}/calls/$callId/listen-token',
        options: Options(
          headers: {'Accept': 'application/json'},
          validateStatus: (status) => status != null && status < 500,
        ),
      );

      if (response.statusCode != 200) {
        throw Exception("Failed to get token: ${response.data}");
      }

      final token = response.data['token'];
      final wsUrl = response.data['ws_url'];

      AppLogger.logger.i("Got LiveKit token for silent listen-in.");

      // 2. Connect to LiveKit Room
      _room = Room();
      
      // Listen to events
      _listener = _room!.createListener();
      _listener!.listen(_onRoomEvent);

      await _room!.connect(
        wsUrl,
        token,
        roomOptions: const RoomOptions(
          adaptiveStream: true,
          dynacast: true,
        ),
      );

      AppLogger.logger.i("Connected to LiveKit room for listen-in!");
      
      state = state.copyWith(isLoading: false, isListening: true);
    } catch (e) {
      AppLogger.logger.e("Failed to start Listen-In mode", error: e);
      state = state.copyWith(isLoading: false, error: e.toString());
      stopListening();
    }
  }

  void _onRoomEvent(RoomEvent event) {
    if (event is RoomDisconnectedEvent) {
      AppLogger.logger.w("LiveKit room disconnected.");
      state = state.copyWith(isListening: false);
    } else if (event is TrackSubscribedEvent) {
      AppLogger.logger.i("Subscribed to remote track: ${event.track.sid}");
    }
  }

  Future<void> stopListening() async {
    if (_room != null) {
      await _room!.disconnect();
      if (_listener != null) {
        await _listener!.dispose();
        _listener = null;
      }
      _room!.dispose();
      _room = null;
    }
    state = ListenState(isListening: false, isLoading: false);
  }

  @override
  void dispose() {
    stopListening();
    super.dispose();
  }
}
