enum WebSocketStatus {
  disconnected,
  connecting,
  connected,
}

class WebSocketState {
  final WebSocketStatus status;

  final String deviceId;

  const WebSocketState({
    required this.status,
    required this.deviceId,
  });

  factory WebSocketState.initial() {
    return const WebSocketState(
      status: WebSocketStatus.disconnected,
      deviceId: "",
    );
  }

  WebSocketState copyWith({
    WebSocketStatus? status,
    String? deviceId,
  }) {
    return WebSocketState(
      status: status ?? this.status,
      deviceId: deviceId ?? this.deviceId,
    );
  }
}