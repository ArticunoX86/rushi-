import 'websocket_event.dart';
import 'websocket_event_type.dart';

class WebSocketEventParser {
  WebSocketEventParser._();

  static WebSocketEvent parse(
    Map<String, dynamic> json,
  ) {
    final action = (json["action"] ?? "")
        .toString()
        .toUpperCase();

    WebSocketEventType type;

    switch (action) {
      // ===================================================
      // Connection
      // ===================================================

      case "CONNECTED":
        type = WebSocketEventType.connected;
        break;

      case "DISCONNECTED":
        type = WebSocketEventType.disconnected;
        break;

      case "PING":
        type = WebSocketEventType.ping;
        break;

      case "PONG":
        type = WebSocketEventType.pong;
        break;

      case "ERROR":
        type = WebSocketEventType.error;
        break;

      // ===================================================
      // Calls
      // ===================================================

      case "CALL":
      case "CALL_ASSIGNED":
        type = WebSocketEventType.callAssigned;
        break;

      case "CALL_ACCEPTED":
        type = WebSocketEventType.callAccepted;
        break;

      case "CALL_REJECTED":
        type = WebSocketEventType.callRejected;
        break;

      case "CALL_STARTED":
        type = WebSocketEventType.callStarted;
        break;

      case "CALL_ENDED":
        type = WebSocketEventType.callEnded;
        break;

      case "CALL_COMPLETED":
        type = WebSocketEventType.callCompleted;
        break;

      case "CALL_CANCELLED":
        type = WebSocketEventType.callCancelled;
        break;

      // ===================================================
      // Device
      // ===================================================

      case "DEVICE_ONLINE":
        type = WebSocketEventType.deviceOnline;
        break;

      case "DEVICE_OFFLINE":
        type = WebSocketEventType.deviceOffline;
        break;

      case "DEVICE_STATUS":
        type = WebSocketEventType.deviceStatus;
        break;

      // ===================================================
      // AI
      // ===================================================

      case "AI_LISTENING":
        type = WebSocketEventType.aiListening;
        break;

      case "AI_THINKING":
        type = WebSocketEventType.aiThinking;
        break;

      case "AI_SPEAKING":
        type = WebSocketEventType.aiSpeaking;
        break;

      case "TRANSCRIPT":
        type = WebSocketEventType.transcript;
        break;

      // ===================================================
      // Unknown
      // ===================================================

      default:
        type = WebSocketEventType.unknown;
        break;
    }

    return WebSocketEvent.create(
      type: type,
      payload: json,
    );
  }
}