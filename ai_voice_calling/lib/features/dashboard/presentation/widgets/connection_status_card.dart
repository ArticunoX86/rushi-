import 'package:flutter/material.dart';

import '../../../../core/widgets/app_card.dart';

class ConnectionStatusCard extends StatelessWidget {
  final bool backendConnected;
  final bool websocketConnected;

  const ConnectionStatusCard({
    super.key,
    required this.backendConnected,
    required this.websocketConnected,
  });

  Widget buildConnectionTile(BuildContext context, {
    required IconData icon,
    required String title,
    required bool connected,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 14),
      child: Row(
        children: [
          Container(
            width: 46,
            height: 46,
            decoration: BoxDecoration(
              color: connected
                  ? Colors.green.shade50
                  : Colors.red.shade50,
              borderRadius: BorderRadius.circular(14),
            ),
            child: Icon(
              icon,
              color: connected
                  ? Colors.green
                  : Colors.red,
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
                  connected ? "Connected" : "Offline",
                  style: TextStyle(
                    color: connected
                        ? Colors.green.shade700
                        : Colors.red.shade700,
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
              ],
            ),
          ),

          Icon(
            connected
                ? Icons.check_circle
                : Icons.cancel,
            color: connected
                ? Colors.green
                : Colors.red,
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(
                Icons.wifi,
                color: Colors.blue,
              ),

              SizedBox(width: 10),

              Text(
                "System Status",
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),

          const SizedBox(height: 20),

          buildConnectionTile(context, 
            icon: Icons.cloud_done,
            title: "Backend",
            connected: backendConnected,
          ),

          const Divider(),

          buildConnectionTile(context, 
            icon: Icons.wifi,
            title: "WebSocket",
            connected: websocketConnected,
          ),
        ],
      ),
    );
  }
}