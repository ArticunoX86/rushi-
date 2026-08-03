import 'dart:async';

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/logger/app_logger.dart';
import '../../../core/websocket/websocket_event_router.dart';
import '../../../core/websocket/websocket_event_type.dart';
import '../../dashboard/providers/dashboard_providers.dart';
import '../models/call_job.dart';
import '../providers/calls_provider.dart';

class CallEventListener {
  CallEventListener._();

  static final CallEventListener instance =
      CallEventListener._();

  StreamSubscription? _subscription;

  void start(
    WidgetRef ref,
  ) {
    if (_subscription != null) {
      return;
    }

    _subscription =
        WebSocketEventRouter.instance.stream.listen(
      (event) {
        switch (event.type) {
          // =====================================================
          // NEW CALL
          // =====================================================

          case WebSocketEventType.callAssigned:
            _handleCallAssigned(
              ref,
              event.payload,
            );
            break;

          // =====================================================
          // CALL STARTED
          // =====================================================

          case WebSocketEventType.callStarted:
            _handleCallStarted(
              ref,
              event.payload,
            );
            break;

          // =====================================================
          // CALL ENDED / COMPLETED
          // =====================================================

          case WebSocketEventType.callEnded:
          case WebSocketEventType.callCompleted:
            _handleCallEnded(
              ref,
              event.payload,
            );
            break;

          // =====================================================
          // CALL CANCELLED
          // =====================================================

          case WebSocketEventType.callCancelled:
            _handleCallCancelled(
              ref,
              event.payload,
            );
            break;

          default:
            break;
        }
      },
    );

    AppLogger.logger.i(
      "Call Event Listener Started",
    );
  }

  void stop() {
    _subscription?.cancel();
    _subscription = null;

    AppLogger.logger.i(
      "Call Event Listener Stopped",
    );
  }

  // =====================================================
  // CALL ASSIGNED
  // =====================================================

  void _handleCallAssigned(
    WidgetRef ref,
    Map<String, dynamic> payload,
  ) {
    final data =
        payload["payload"] as Map<String, dynamic>? ??
            payload;

    final job = CallJob(
      id: (data["id"] ?? data["call_id"] ?? "")
          .toString(),
      customerName:
          (data["customer_name"] ?? "Unknown")
              .toString(),
      phoneNumber:
          (data["phone_number"] ?? data["phone"] ?? "")
              .toString(),
      status:
          (data["status"] ?? "PENDING")
              .toString(),
      priority:
          (data["priority"] ?? "NORMAL")
              .toString(),
      scriptName:
          (data["script_name"] ??
                  "Default Script")
              .toString(),
      createdAt: data["created_at"] != null
          ? DateTime.parse(
              data["created_at"].toString(),
            )
          : DateTime.now(),
    );

    ref
        .read(callsProvider.notifier)
        .addCallJob(job);

    AppLogger.logger.i(
      "New Call Assigned: ${job.customerName}",
    );
  }

  // =====================================================
  // CALL STARTED
  // =====================================================

  void _handleCallStarted(
    WidgetRef ref,
    Map<String, dynamic> payload,
  ) {
    final data =
        payload["payload"] as Map<String, dynamic>? ??
            payload;

    final callId =
        (data["call_id"] ?? data["id"] ?? "")
            .toString();

    ref
        .read(callsProvider.notifier)
        .removeCallJob(callId);

    AppLogger.logger.i(
      "Call Started: $callId",
    );
  }

  // =====================================================
  // CALL CANCELLED
  // =====================================================

  void _handleCallCancelled(
    WidgetRef ref,
    Map<String, dynamic> payload,
  ) {
    final data =
        payload["payload"] as Map<String, dynamic>? ??
            payload;

    final callId =
        (data["call_id"] ?? data["id"] ?? "")
            .toString();

    ref
        .read(callsProvider.notifier)
        .removeCallJob(callId);

    AppLogger.logger.i(
      "Call Cancelled: $callId",
    );
  }

  // =====================================================
  // CALL ENDED / COMPLETED INSTANT REFRESH
  // =====================================================

  void _handleCallEnded(
    WidgetRef ref,
    Map<String, dynamic> payload,
  ) {
    final data =
        payload["payload"] as Map<String, dynamic>? ??
            payload;

    final callId =
        (data["call_id"] ?? data["id"] ?? "")
            .toString();

    if (callId.isNotEmpty) {
      ref
          .read(callsProvider.notifier)
          .removeCallJob(callId);
    }

    // Instantly invalidate Dashboard and Calls providers for immediate UI update!
    ref.invalidate(dashboardProvider);
    ref.invalidate(callsProvider);

    AppLogger.logger.i(
      "⚡ CALL ENDED / COMPLETED — INSTANT REFRESH TRIGGERED: $callId",
    );
  }
}