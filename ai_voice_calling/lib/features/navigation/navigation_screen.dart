import 'package:flutter/material.dart';
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
      body: IndexedStack(
        index: currentIndex,
        children: screens,
      ),

      bottomNavigationBar: Theme(
        data: Theme.of(context).copyWith(
          navigationBarTheme: NavigationBarThemeData(
            backgroundColor: Colors.white,
            elevation: 8,
            shadowColor: Colors.black12,
            indicatorColor: Color(0xFF1B8B4B).withOpacity(0.15),
            iconTheme: WidgetStateProperty.resolveWith((states) {
              if (states.contains(WidgetState.selected)) {
                return const IconThemeData(color: Color(0xFF1B8B4B));
              }
              return IconThemeData(color: Colors.grey.shade600);
            }),
            labelTextStyle: WidgetStateProperty.resolveWith((states) {
              if (states.contains(WidgetState.selected)) {
                return const TextStyle(color: Color(0xFF1B8B4B), fontWeight: FontWeight.bold, fontSize: 11);
              }
              return TextStyle(color: Colors.grey.shade600, fontSize: 11);
            }),
          ),
        ),
        child: NavigationBar(
          selectedIndex: currentIndex,
          onDestinationSelected: (index) {
            setState(() {
              currentIndex = index;
            });
          },

        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.dashboard_outlined),
            selectedIcon: Icon(Icons.dashboard),
            label: "Dashboard",
          ),

          NavigationDestination(
            icon: Icon(Icons.call_outlined),
            selectedIcon: Icon(Icons.call),
            label: "Calls",
          ),

          NavigationDestination(
            icon: Icon(Icons.record_voice_over_outlined),
            selectedIcon: Icon(Icons.record_voice_over),
            label: "Transcripts",
          ),

          NavigationDestination(
            icon: Icon(Icons.hearing_outlined),
            selectedIcon: Icon(Icons.hearing),
            label: "Audit",
          ),

          NavigationDestination(
            icon: Icon(Icons.bar_chart_outlined),
            selectedIcon: Icon(Icons.bar_chart),
            label: "Analytics",
          ),

          NavigationDestination(
            icon: Icon(Icons.cloud_outlined),
            selectedIcon: Icon(Icons.cloud),
            label: "Salesforce",
          ),

          NavigationDestination(
            icon: Icon(Icons.settings_outlined),
            selectedIcon: Icon(Icons.settings),
            label: "Settings",
          ),
        ],
      ),
    ),
    );
  }
}