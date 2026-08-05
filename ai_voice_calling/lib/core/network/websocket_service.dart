import 'dart:async';
import 'dart:convert';

import 'package:web_socket_channel/web_socket_channel.dart';

import '../config/app_config.dart';
import '../logger/app_logger.dart';
import '../websocket/websocket_event.dart';
import '../websocket/websocket_event_parser.dart';
import '../websocket/websocket_event_router.dart';
import '../notifications/push_notification_overlay.dart';

class WebSocketService {
  WebSocketService._();

  static final WebSocketService instance =
      WebSocketService._();

  WebSocketChannel? _channel;

  StreamSubscription? _subscription;

  bool _connected = false;

  bool get isConnected => _connected;

  final StreamController<bool> _statusController = StreamController<bool>.broadcast();
  Stream<bool> get onStatusChanged => _statusController.stream;

  bool _userClosed = false;
  Timer? _reconnectTimer;
  String? _lastDeviceId;

  Future<void> connect({
    required String deviceId,
  }) async {
    _lastDeviceId = deviceId;
    _userClosed = false;
    _reconnectTimer?.cancel();

    if (_connected) {
      AppLogger.logger.i(
        "WebSocket already connected.",
      );
      return;
    }

    final uri = Uri.parse(
      "${AppConfig.websocketUrl}/device/connect/$deviceId",
    );

    AppLogger.logger.i(
      "Connecting to $uri",
    );

    try {
      _channel = WebSocketChannel.connect(uri);

      _connected = true;
      _statusController.add(true);

      _subscription = _channel!.stream.listen(
        _onMessage,
        onDone: _onDisconnected,
        onError: _onError,
      );

      AppLogger.logger.i(
        "WebSocket Connected",
      );
    } catch (e) {
      _connected = false;
      _statusController.add(false);
      AppLogger.logger.e("WebSocket initial connection failed", error: e);
      _scheduleReconnect();
    }
  }

  // =====================================================
  // RECEIVE MESSAGE
  // =====================================================

  void _onMessage(dynamic message) {
    try {
      AppLogger.logger.i(
        "Raw Message: $message",
      );

      final Map<String, dynamic> json =
          jsonDecode(message);

      final WebSocketEvent event =
          WebSocketEventParser.parse(
        json,
      );

      AppLogger.logger.i(
        "Parsed Event: ${event.type}",
      );

      if (json['action'] == 'HOT_LEAD_ALERT' || json['event'] == 'HOT_LEAD_ALERT') {
        NotificationEventBus.fire(json['payload'] ?? {});
      }

      WebSocketEventRouter.instance.dispatch(
        event,
      );
    } catch (e, stackTrace) {
      AppLogger.logger.e(
        "Failed to process WebSocket message",
        error: e,
        stackTrace: stackTrace,
      );
    }
  }

  // =====================================================
  // DISCONNECTED
  // =====================================================

  void _onDisconnected() {
    _connected = false;
    _statusController.add(false);

    AppLogger.logger.w(
      "WebSocket disconnected.",
    );
    _scheduleReconnect();
  }

  // =====================================================
  // ERROR
  // =====================================================

  void _onError(dynamic error) {
    _connected = false;
    _statusController.add(false);

    AppLogger.logger.e(
      "WebSocket error",
      error: error,
    );
    _scheduleReconnect();
  }

  void _scheduleReconnect() {
    if (_userClosed || _lastDeviceId == null) return;
    _reconnectTimer?.cancel();
    _reconnectTimer = Timer(const Duration(seconds: 5), () {
      AppLogger.logger.i("Attempting to reconnect WebSocket...");
      connect(deviceId: _lastDeviceId!);
    });
  }

  // =====================================================
  // SEND
  // =====================================================

  void send(
    Map<String, dynamic> message,
  ) {
    if (!_connected) {
      AppLogger.logger.w(
        "Cannot send. Socket disconnected.",
      );
      return;
    }

    _channel!.sink.add(
      jsonEncode(message),
    );
  }

  // =====================================================
  // DISCONNECT
  // =====================================================

  Future<void> disconnect() async {
    _userClosed = true;
    _reconnectTimer?.cancel();
    _reconnectTimer = null;

    await _subscription?.cancel();

    await _channel?.sink.close();

    _subscription = null;
    _channel = null;

    _connected = false;

    AppLogger.logger.i(
      "WebSocket Closed",
    );
  }
}