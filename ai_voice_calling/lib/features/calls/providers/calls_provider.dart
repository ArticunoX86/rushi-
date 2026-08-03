import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/call_job.dart';

final callsProvider =
    StateNotifierProvider<CallsNotifier, CallsState>(
  (ref) {
    return CallsNotifier();
  },
);

class CallsNotifier extends StateNotifier<CallsState> {
  CallsNotifier() : super(const CallsState());

  void setCallJobs(List<CallJob> jobs) {
    state = state.copyWith(
      jobs: jobs,
    );
  }

  void addCallJob(CallJob job) {
    state = state.copyWith(
      jobs: [
        job,
        ...state.jobs,
      ],
    );
  }

  void removeCallJob(String jobId) {
    state = state.copyWith(
      jobs: state.jobs
          .where(
            (job) => job.id != jobId,
          )
          .toList(),
    );
  }

  void clearJobs() {
    state = state.copyWith(
      jobs: [],
    );
  }
}

class CallsState {
  final List<CallJob> jobs;

  const CallsState({
    this.jobs = const [],
  });

  bool get hasJobs => jobs.isNotEmpty;

  int get totalJobs => jobs.length;

  CallsState copyWith({
    List<CallJob>? jobs,
  }) {
    return CallsState(
      jobs: jobs ?? this.jobs,
    );
  }
}