import 'package:flutter/material.dart';

import '../../../../core/widgets/app_card.dart';

class DeviceInfoCard extends StatelessWidget {
  final String deviceName;
  final String deviceId;
  final String phoneNumber;

  const DeviceInfoCard({
    super.key,
    required this.deviceName,
    required this.deviceId,
    required this.phoneNumber,
  });

  Widget buildInfoTile({
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
              color: Colors.blue.shade50,
              borderRadius: BorderRadius.circular(14),
            ),
            child: Icon(
              icon,
              color: Colors.blue,
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
                  overflow: TextOverflow.ellipsis,
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
                Icons.phone_android,
                color: Colors.blue,
              ),

              SizedBox(width: 10),

              Text(
                "Device Information",
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),

            ],
          ),

          const SizedBox(height: 20),

          buildInfoTile(
            icon: Icons.devices,
            title: "Device",
            value: deviceName,
          ),

          const Divider(),

          buildInfoTile(
            icon: Icons.fingerprint,
            title: "Device ID",
            value: deviceId,
          ),

          const Divider(),

          buildInfoTile(
            icon: Icons.phone,
            title: "Phone Number",
            value: phoneNumber,
          ),
        ],
      ),
    );
  }
}