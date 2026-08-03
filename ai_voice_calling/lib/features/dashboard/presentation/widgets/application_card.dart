import 'package:flutter/material.dart';

import '../../../../core/widgets/app_card.dart';
import '../../../../core/widgets/app_section_title.dart';

class ApplicationCard extends StatelessWidget {
  final String version;

  const ApplicationCard({
    super.key,
    required this.version,
  });

  @override
  Widget build(BuildContext context) {
    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const AppSectionTitle(
            title: "Application",
          ),

          Row(
            children: [
              const Icon(
                Icons.info,
                color: Colors.deepPurple,
              ),

              const SizedBox(width: 16),

              Expanded(
                child: Text(
                  version,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}