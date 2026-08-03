import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../device/device_service.dart';
import 'repositories/device_repository.dart';
import 'websocket_service.dart';
import 'websocket_state.dart';

final websocketProvider =
    StateNotifierProvider<WebSocketNotifier, WebSocketState>(
  (ref) {
    return WebSocketNotifier();
  },
);

class WebSocketNotifier extends StateNotifier<WebSocketState> {
  WebSocketNotifier() : super(WebSocketState.initial()) {
    _service.onStatusChanged.listen((connected) {
      state = state.copyWith(
        status: connected ? WebSocketStatus.connected : WebSocketStatus.disconnected,
      );
    });
  }

  final WebSocketService _service = WebSocketService.instance;

  final DeviceService _deviceService = DeviceService.instance;

  Future<void> connect() async {
    if (state.status == WebSocketStatus.connected) {
      return;
    }

    state = state.copyWith(
      status: WebSocketStatus.connecting,
    );

    // =====================================================
    // GET PERMANENT DEVICE ID
    // =====================================================

    final deviceId = await _deviceService.getDeviceId();

    // =====================================================
    // REGISTER DEVICE IN BACKEND
    // =====================================================

    await DeviceRepository.instance.registerDevice();

    // =====================================================
    // CONNECT WEBSOCKET
    // =====================================================

    await _service.connect(
      deviceId: deviceId,
    );

    state = state.copyWith(
      status: WebSocketStatus.connected,
      deviceId: deviceId,
    );
  }

  Future<void> disconnect() async {
    await _service.disconnect();

    state = state.copyWith(
      status: WebSocketStatus.disconnected,
    );
  }
}