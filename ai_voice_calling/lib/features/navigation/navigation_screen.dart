import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../analytics/presentation/analytics_screen.dart';
import '../calls/presentation/calls_screen.dart';
import '../calls/services/call_event_listener.dart';
import '../dashboard/presentation/dashboard_screen.dart';
import '../settings/presentation/settings_screen.dart';
import '../transcripts/presentation/transcripts_screen.dart';
import '../supervisor/presentation/audit_console_screen.dart';
import '../supervisor/presentation/salesforce_sync_screen.dart';

class NavigationScreen extends ConsumerStatefulWidget {
  const NavigationScreen({super.key});

  @override
  ConsumerState<NavigationScreen> createState() =>
      _NavigationScreenState();
}

class _NavigationScreenState
    extends ConsumerState<NavigationScreen> {
  int currentIndex = 0;

  final List<Widget> screens = const [
    DashboardScreen(),
    CallsScreen(),
    TranscriptsScreen(),
    AuditConsoleScreen(),
    AnalyticsScreen(),
    SalesforceSyncScreen(),
    SettingsScreen(),
  ];

  @override
  void initState() {
    super.initState();

    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return;

      CallEventListener.instance.start(ref);
    });
  }

  @override
  void dispose() {
    CallEventListener.instance.stop();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBody: true, // Allows body to flow under the floating nav bar
      body: SafeArea(
        bottom: false,
        child: IndexedStack(
          index: currentIndex,
          children: screens,
        ),
      ),
      bottomNavigationBar: SafeArea(
        child: Padding(
          padding: const EdgeInsets.only(left: 16, right: 16, bottom: 16),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(32),
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 12, sigmaY: 12),
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.6),
                  borderRadius: BorderRadius.circular(32),
                  border: Border.all(
                    color: Colors.white.withOpacity(0.6),
                    width: 1.5,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: const Color(0xFF7C3AED).withOpacity(0.15),
                      blurRadius: 20,
                      offset: const Offset(0, 8),
                    )
                  ],
                ),
                child: Theme(
                  data: Theme.of(context).copyWith(
                    navigationBarTheme: NavigationBarThemeData(
                      backgroundColor: Colors.transparent,
                      surfaceTintColor: Colors.transparent,
                      elevation: 0,
                      indicatorColor: const Color(0xFF7C3AED).withOpacity(0.2),
                      indicatorShape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                      iconTheme: WidgetStateProperty.resolveWith((states) {
                        if (states.contains(WidgetState.selected)) {
                          return const IconThemeData(color: Color(0xFF7C3AED), size: 22);
                        }
                        return IconThemeData(color: Colors.grey.shade600, size: 22);
                      }),
                      labelTextStyle: WidgetStateProperty.resolveWith((states) {
                        if (states.contains(WidgetState.selected)) {
                          return const TextStyle(color: Color(0xFF7C3AED), fontWeight: FontWeight.bold, fontSize: 10);
                        }
                        return TextStyle(color: Colors.grey.shade600, fontSize: 10);
                      }),
                    ),
                  ),
                  child: MediaQuery.removePadding(
                    context: context,
                    removeBottom: true,
                    child: NavigationBar(
                      height: 65, // Sleek height
                      selectedIndex: currentIndex,
                      onDestinationSelected: (index) {
                        HapticFeedback.lightImpact();
                        setState(() {
                          currentIndex = index;
                        });
                      },
                      destinations: const [
                        NavigationDestination(
                          icon: Icon(Icons.dashboard_outlined),
                          selectedIcon: Icon(Icons.dashboard),
                          label: "Dash",
                        ),
                        NavigationDestination(
                          icon: Icon(Icons.call_outlined),
                          selectedIcon: Icon(Icons.call),
                          label: "Calls",
                        ),
                        NavigationDestination(
                          icon: Icon(Icons.record_voice_over_outlined),
                          selectedIcon: Icon(Icons.record_voice_over),
                          label: "Recs",
                        ),
                        NavigationDestination(
                          icon: Icon(Icons.hearing_outlined),
                          selectedIcon: Icon(Icons.hearing),
                          label: "Audit",
                        ),
                        NavigationDestination(
                          icon: Icon(Icons.bar_chart_outlined),
                          selectedIcon: Icon(Icons.bar_chart),
                          label: "Stats",
                        ),
                        NavigationDestination(
                          icon: Icon(Icons.cloud_outlined),
                          selectedIcon: Icon(Icons.cloud),
                          label: "Sync",
                        ),
                        NavigationDestination(
                          icon: Icon(Icons.settings_outlined),
                          selectedIcon: Icon(Icons.settings),
                          label: "Config",
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}