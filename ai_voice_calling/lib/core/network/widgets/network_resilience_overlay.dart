import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../network_provider.dart';

class NetworkResilienceOverlay extends ConsumerWidget {
  final Widget child;

  const NetworkResilienceOverlay({super.key, required this.child});

  static const Color _emerald = Color(0xFF7C3AED);
  static const Color _charcoal = Color(0xFF172554);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isOffline = ref.watch(networkStatusProvider);

    return Directionality(
      textDirection: TextDirection.ltr,
      child: Stack(
        children: [
          child,
          if (isOffline)
            Positioned.fill(
              child: BackdropFilter(
                filter: ImageFilter.blur(sigmaX: 5.0, sigmaY: 5.0),
                child: Container(
                  color: _charcoal.withOpacity(0.85),
                  child: Center(
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 40),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(
                            Icons.wifi_off_rounded,
                            color: _emerald,
                            size: 64,
                          ),
                          const SizedBox(height: 24),
                          const Text(
                            'Backend Offline',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 24,
                              fontWeight: FontWeight.bold,
                              decoration: TextDecoration.none,
                            ),
                          ),
                          const SizedBox(height: 12),
                          const Text(
                            'Unable to connect to the NexaVoice server. We are automatically trying to reconnect...',
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              color: Colors.white70,
                              fontSize: 15,
                              height: 1.5,
                              decoration: TextDecoration.none,
                            ),
                          ),
                          const SizedBox(height: 32),
                          const CircularProgressIndicator(
                            valueColor: AlwaysStoppedAnimation<Color>(_emerald),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }
}
