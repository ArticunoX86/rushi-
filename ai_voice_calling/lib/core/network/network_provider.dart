import 'dart:async';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'dio_client.dart';
import 'websocket_service.dart';

final networkStatusProvider = StateNotifierProvider<NetworkStatusNotifier, bool>((ref) {
  return NetworkStatusNotifier();
});

class NetworkStatusNotifier extends StateNotifier<bool> {
  NetworkStatusNotifier() : super(false) {
    _initListeners();
  }

  StreamSubscription? _dioSub;
  StreamSubscription? _wsSub;

  void _initListeners() {
    // Listen to Dio REST API connection errors
    _dioSub = DioClient.instance.onNetworkStatusChanged.listen((isOffline) {
      if (state != isOffline) {
        state = isOffline;
      }
    });

    // Listen to WebSocket connection drops
    _wsSub = WebSocketService.instance.onStatusChanged.listen((isConnected) {
      final isOffline = !isConnected;
      if (state != isOffline) {
        state = isOffline;
      }
    });
  }

  @override
  void dispose() {
    _dioSub?.cancel();
    _wsSub?.cancel();
    super.dispose();
  }
}
