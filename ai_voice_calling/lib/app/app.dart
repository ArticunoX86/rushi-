import 'package:flutter/material.dart';

import '../core/network/widgets/network_resilience_overlay.dart';
import '../core/startup/startup_gate.dart';
import 'theme/app_theme.dart';

class AIVoiceCallingApp extends StatelessWidget {
  const AIVoiceCallingApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Voice Calling',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      builder: (context, child) {
        return NetworkResilienceOverlay(
          child: child ?? const SizedBox.shrink(),
        );
      },
      home: const StartupGate(),
    );
  }
}