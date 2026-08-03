import 'package:flutter/material.dart';

class AppStatusBadge extends StatelessWidget {
  final bool online;

  final String text;

  const AppStatusBadge({
    super.key,
    required this.online,
    required this.text,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: 14,
        vertical: 8,
      ),
      decoration: BoxDecoration(
        color: online
            ? Colors.green.shade50
            : Colors.red.shade50,
        borderRadius: BorderRadius.circular(
          30,
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            Icons.circle,
            size: 10,
            color: online
                ? Colors.green
                : Colors.red,
          ),
          const SizedBox(width: 8),
          Text(
            text,
            style: TextStyle(
              color: online
                  ? Colors.green.shade700
                  : Colors.red.shade700,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }
}