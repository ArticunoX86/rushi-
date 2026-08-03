import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../providers/calls_provider.dart';
import 'widgets/call_job_card.dart';
import 'widgets/empty_calls_widget.dart';
import 'widgets/waiting_for_jobs_widget.dart';

class CallsScreen extends ConsumerWidget {
  const CallsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final calls = ref.watch(callsProvider);

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: const Text("Calls", style: TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold)),
        centerTitle: true,
      ),

      body: SafeArea(
        child: Column(
          children: [
            const SizedBox(height: 20),

            Padding(
              padding: const EdgeInsets.symmetric(
                horizontal: 20,
              ),
              child: WaitingForJobsWidget(
                totalJobs: calls.totalJobs,
              ),
            ),

            const SizedBox(height: 20),

            Expanded(
              child: calls.hasJobs
                  ? ListView.separated(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 20,
                      ),
                      itemCount: calls.jobs.length,
                      separatorBuilder: (_, __) =>
                          const SizedBox(height: 16),
                      itemBuilder: (context, index) {
                        return CallJobCard(
                          job: calls.jobs[index],
                        );
                      },
                    )
                  : const EmptyCallsWidget(),
            ),
          ],
        ),
      ),
    );
  }
}