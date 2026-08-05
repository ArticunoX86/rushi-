import 'package:flutter/material.dart';

class WaitingForJobsWidget extends StatelessWidget {
  final int totalJobs;

  const WaitingForJobsWidget({
    super.key,
    required this.totalJobs,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Row(
          children: [
            const CircleAvatar(
              radius: 28,
              backgroundColor: Color(0xFFE8F0FE),
              child: Icon(
                Icons.wifi,
                color: Color(0xFF7C3AED),
                size: 30,
              ),
            ),

            const SizedBox(width: 16),

            Expanded(
              child: Column(
                crossAxisAlignment:
                    CrossAxisAlignment.start,
                children: [
                  const Text(
                    "Waiting for Call Jobs",
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),

                  const SizedBox(height: 6),

                  const Text(
                    "Connected to backend",
                    style: TextStyle(
                      color: Colors.grey,
                    ),
                  ),
                ],
              ),
            ),

            CircleAvatar(
              backgroundColor:
                  const Color(0xFF7C3AED),
              child: Text(
                totalJobs.toString(),
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}