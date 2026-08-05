import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';

class DashboardHeader extends StatelessWidget {
  final bool online;

  const DashboardHeader({
    super.key,
    required this.online,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(28),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [
            Color(0xFF7C3AED),
            Color(0xFF5B21B6), // Deeper violet for richer contrast
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(28),
        boxShadow: [
          BoxShadow(
            color: const Color(0xFF7C3AED).withOpacity(0.3),
            blurRadius: 24,
            offset: const Offset(0, 12),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(
            Icons.support_agent_rounded,
            color: Colors.white,
            size: 56,
          ).animate(onPlay: (controller) => controller.repeat()).shimmer(duration: 2000.ms, color: Colors.white.withOpacity(0.4)),

          const SizedBox(height: 24),

          const Text(
            "AI Voice Calling",
            style: TextStyle(
              color: Colors.white,
              fontSize: 32,
              fontWeight: FontWeight.bold,
              letterSpacing: -0.5,
            ),
          ).animate().fadeIn(duration: 600.ms).slideY(begin: 0.2, end: 0, curve: Curves.easeOutQuad),

          const SizedBox(height: 6),

          const Text(
            "Commercial AI Calling Platform",
            style: TextStyle(
              color: Colors.white70,
              fontSize: 16,
            ),
          ).animate().fadeIn(delay: 200.ms, duration: 600.ms).slideY(begin: 0.2, end: 0, curve: Curves.easeOutQuad),

          const SizedBox(height: 28),

          Container(
            padding: const EdgeInsets.symmetric(
              horizontal: 16,
              vertical: 10,
            ),
            decoration: BoxDecoration(
              color: Colors.white.withAlpha(35),
              borderRadius: BorderRadius.circular(30),
              border: Border.all(color: Colors.white.withAlpha(50)),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  Icons.circle,
                  color: online ? Colors.greenAccent : Colors.redAccent,
                  size: 12,
                ).animate(onPlay: (controller) => controller.repeat()).shimmer(duration: 1500.ms, delay: 500.ms),

                const SizedBox(width: 10),

                Text(
                  online ? "Device Online" : "Offline",
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ).animate().fadeIn(delay: 400.ms, duration: 600.ms),
        ],
      ),
    );
  }
}