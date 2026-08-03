import 'package:flutter/material.dart';

class DashboardHeader extends StatelessWidget {
  final bool online;

  const DashboardHeader({
    super.key,
    required this.online,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [
            Color(0xFF1B8B4B),
            Color(0xFF26A35A),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(
            color: Colors.blue.withAlpha(60),
            blurRadius: 20,
            offset: const Offset(0, 10),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(
            Icons.support_agent_rounded,
            color: Colors.white,
            size: 50,
          ),

          const SizedBox(height: 20),

          const Text(
            "AI Voice Calling",
            style: TextStyle(
              color: Colors.white,
              fontSize: 30,
              fontWeight: FontWeight.bold,
            ),
          ),

          const SizedBox(height: 8),

          const Text(
            "Commercial AI Calling Platform",
            style: TextStyle(
              color: Colors.white70,
              fontSize: 16,
            ),
          ),

          const SizedBox(height: 24),

          Container(
            padding: const EdgeInsets.symmetric(
              horizontal: 16,
              vertical: 10,
            ),
            decoration: BoxDecoration(
              color: Colors.white.withAlpha(35),
              borderRadius: BorderRadius.circular(30),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  Icons.circle,
                  color: online ? Colors.greenAccent : Colors.redAccent,
                  size: 12,
                ),

                const SizedBox(width: 10),

                Text(
                  online ? "Device Online" : "Offline",
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}