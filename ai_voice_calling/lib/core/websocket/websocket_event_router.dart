import 'dart:async';

import 'websocket_event.dart';

class WebSocketEventRouter {
  WebSocketEventRouter._();

  static final WebSocketEventRouter instance =
      WebSocketEventRouter._();

  final StreamController<WebSocketEvent> _controller =
      StreamController<WebSocketEvent>.broadcast();

  Stream<WebSocketEvent> get stream => _controller.stream;

  void dispatch(WebSocketEvent event) {
    _controller.add(event);
  }

  Future<void> dispose() async {
    await _controller.close();
  }
}