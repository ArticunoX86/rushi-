import 'package:flutter/material.dart';

import '../../../../core/widgets/app_card.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/dashboard_providers.dart';
import '../../../supervisor/services/livekit_listen_service.dart';

class CurrentCallCard extends ConsumerWidget {
  final String status;

  final String? activeCallId;

  const CurrentCallCard({
    super.key,
    required this.status,
    this.activeCallId,
  });

  Widget buildInfoRow({
    required IconData icon,
    required String title,
    required String value,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 14),
      child: Row(
        children: [
          Container(
            width: 46,
            height: 46,
            decoration: BoxDecoration(
              color: Colors.orange.shade50,
              borderRadius: BorderRadius.circular(14),
            ),
            child: Icon(
              icon,
              color: Colors.orange,
            ),
          ),

          const SizedBox(width: 16),

          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    color: Colors.grey.shade600,
                    fontSize: 13,
                  ),
                ),

                const SizedBox(height: 4),

                Text(
                  value,
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final listenState = ref.watch(livekitListenProvider);

    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(
                Icons.call,
                color: Colors.orange,
              ),

              SizedBox(width: 10),

              Text(
                "Current Call",
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),

          const SizedBox(height: 20),

          buildInfoRow(
            icon: Icons.phone_in_talk,
            title: "Status",
            value: status,
          ),

          const Divider(),

          buildInfoRow(
            icon: Icons.person,
            title: "Customer",
            value: "No Active Customer",
          ),

          const Divider(),

          buildInfoRow(
            icon: Icons.timer,
            title: "Duration",
            value: "00:00",
          ),

          if (activeCallId != null) ...[
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: listenState.isListening 
                      ? Colors.red.shade50 
                      : Colors.orange.shade50,
                  foregroundColor: listenState.isListening 
                      ? Colors.red 
                      : Colors.orange,
                  elevation: 0,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(14),
                  ),
                ),
                onPressed: () {
                  if (listenState.isListening) {
                    ref.read(livekitListenProvider.notifier).stopListening();
                  } else {
                    ref.read(livekitListenProvider.notifier).startListening(activeCallId!);
                  }
                },
                icon: listenState.isLoading
                    ? const SizedBox(
                        width: 20, height: 20, 
                        child: CircularProgressIndicator(strokeWidth: 2)
                      )
                    : Icon(listenState.isListening ? Icons.stop_circle : Icons.headset_mic),
                label: Text(
                  listenState.isLoading
                      ? "Connecting to Room..."
                      : listenState.isListening
                          ? "Stop Listening"
                          : "Listen In to Call",
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}