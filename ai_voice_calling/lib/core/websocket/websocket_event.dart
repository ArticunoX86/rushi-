import 'websocket_event_type.dart';

class WebSocketEvent {
  final WebSocketEventType type;

  final Map<String, dynamic> payload;

  final DateTime timestamp;

  const WebSocketEvent({
    required this.type,
    required this.payload,
    required this.timestamp,
  });

  factory WebSocketEvent.create({
    required WebSocketEventType type,
    required Map<String, dynamic> payload,
  }) {
    return WebSocketEvent(
      type: type,
      payload: payload,
      timestamp: DateTime.now(),
    );
  }

  T? value<T>(String key) {
    final value = payload[key];

    if (value is T) {
      return value;
    }

    return null;
  }

  bool contains(String key) {
    return payload.containsKey(key);
  }

  @override
  String toString() {
    return '''
WebSocketEvent(
  type: $type,
  payload: $payload,
  timestamp: $timestamp,
)
''';
  }
}