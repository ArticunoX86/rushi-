import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../models/call_job.dart';
import '../../services/call_action_service.dart';
import '../../../../services/native_phone_service.dart';
import '../../providers/calls_provider.dart';
import '../../../../core/logger/app_logger.dart';
import '../../../../services/realtime_audio_service.dart';
import '../screens/active_call_screen.dart';

class CallJobCard extends ConsumerWidget {
  final CallJob job;

  const CallJobCard({
    super.key,
    required this.job,
  });

  Color getPriorityColor() {
    switch (job.priority.toUpperCase()) {
      case "HIGH":
        return Colors.red;

      case "MEDIUM":
        return Colors.orange;

      default:
        return Colors.green;
    }
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(
                    job.customerName,
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                Chip(
                  label: Text(job.priority),
                  backgroundColor:
                      getPriorityColor().withOpacity(0.15),
                  labelStyle: TextStyle(
                    color: getPriorityColor(),
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),

            const SizedBox(height: 10),

            Row(
              children: [
                const Icon(
                  Icons.phone,
                  size: 18,
                  color: Colors.grey,
                ),
                const SizedBox(width: 8),
                Text(job.phoneNumber),
              ],
            ),

            const SizedBox(height: 8),

            Row(
              children: [
                const Icon(
                  Icons.description,
                  size: 18,
                  color: Colors.grey,
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(job.scriptName),
                ),
              ],
            ),

            const SizedBox(height: 18),

            Row(
              children: [
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: () async {
                      try {
                        // Register call_id so realtime streaming knows which session to open
                        RealTimeAudioService.instance.registerCallId(job.id);

                        // Notify backend
                        CallActionService.instance.acceptCall(
                          callId: job.id,
                        );

                        // Remove card from UI
                        ref.read(callsProvider.notifier).removeCallJob(job.id);

                        // Navigate to Active Call UI
                        if (context.mounted) {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => ActiveCallScreen(job: job),
                            ),
                          );
                        }
                      } catch (e, stackTrace) {
                        AppLogger.logger.e(
                          "Failed to make native call",
                          error: e,
                          stackTrace: stackTrace,
                        );
                        if (context.mounted) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text("Failed to make call: $e"),
                              backgroundColor: Colors.redAccent,
                            ),
                          );
                        }
                      }
                    },
                    icon: const Icon(Icons.call),
                    label: const Text("Accept"),
                  ),
                ),

                const SizedBox(width: 12),

                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () {
                      CallActionService.instance.rejectCall(
                        callId: job.id,
                      );

                      // Remove card from UI
                      ref.read(callsProvider.notifier).removeCallJob(job.id);
                    },
                    icon: const Icon(Icons.close),
                    label: const Text("Reject"),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}