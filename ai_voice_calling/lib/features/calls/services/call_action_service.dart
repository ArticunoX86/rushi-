import '../../../core/logger/app_logger.dart';
import '../../../core/network/websocket_service.dart';
import '../../../core/websocket/websocket_event.dart';
import '../../../core/websocket/websocket_event_router.dart';
import '../../../core/websocket/websocket_event_type.dart';

class CallActionService {
  CallActionService._();

  static final CallActionService instance =
      CallActionService._();

  // =====================================================
  // ACCEPT CALL
  // =====================================================

  void acceptCall({
    required String callId,
  }) {
    final message = {
      "action": "CALL_ACCEPTED",
      "payload": {
        "call_id": callId,
      },
    };

    AppLogger.logger.i(
      "Sending CALL_ACCEPTED: $callId",
    );

    WebSocketService.instance.send(message);
  }

  // =====================================================
  // REJECT CALL
  // =====================================================

  void rejectCall({
    required String callId,
  }) {
    final message = {
      "action": "CALL_REJECTED",
      "payload": {
        "call_id": callId,
      },
    };

    AppLogger.logger.i(
      "Sending CALL_REJECTED: $callId",
    );

    WebSocketService.instance.send(message);
  }

  // =====================================================
  // END CALL
  // =====================================================

  void endCall() {
    final message = {
      "action": "CALL_ENDED",
      "payload": {},
    };

    AppLogger.logger.i(
      "Sending CALL_ENDED",
    );

    WebSocketService.instance.send(message);

    // Instant local dispatch so UI updates immediately upon cutting the call
    WebSocketEventRouter.instance.dispatch(
      WebSocketEvent(
        type: WebSocketEventType.callEnded,
        payload: {"action": "CALL_ENDED"},
        timestamp: DateTime.now(),
      ),
    );
  }
}