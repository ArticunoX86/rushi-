import 'package:flutter/material.dart';

import '../../../../core/widgets/app_card.dart';

class CurrentCallCard extends StatelessWidget {
  final String status;

  const CurrentCallCard({
    super.key,
    required this.status,
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
  Widget build(BuildContext context) {
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
        ],
      ),
    );
  }
}