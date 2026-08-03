import 'package:flutter/material.dart';

class EmptyCallsWidget extends StatelessWidget {
  const EmptyCallsWidget({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.call_end_outlined,
              size: 90,
              color: Colors.grey.shade400,
            ),

            const SizedBox(height: 24),

            const Text(
              "No Pending Call Jobs",
              style: TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 12),

            Text(
              "Waiting for the backend to assign a new call.",
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 16,
                color: Colors.grey,
              ),
            ),
          ],
        ),
      ),
    );
  }
}