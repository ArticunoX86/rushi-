import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../features/auth/presentation/login_screen.dart';

import '../../features/logs/providers/dev_logs_provider.dart';

class StartupGate extends ConsumerStatefulWidget {
  const StartupGate({super.key});

  @override
  ConsumerState<StartupGate> createState() =>
      _StartupGateState();
}

class _StartupGateState
    extends ConsumerState<StartupGate> {
  bool _loading = true;

  @override
  void initState() {
    super.initState();

    WidgetsBinding.instance.addPostFrameCallback((_) async {
      if (!mounted) return;

      setState(() {
        _loading = false;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    // Eagerly listen to developer logs
    ref.watch(devLogsProvider);

    if (_loading) {
      return const Scaffold(
        body: Center(
          child: CircularProgressIndicator(),
        ),
      );
    }

    return const LoginScreen();
  }
}