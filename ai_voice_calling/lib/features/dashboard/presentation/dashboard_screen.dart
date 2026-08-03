import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../providers/dashboard_providers.dart';
import 'widgets/application_card.dart';
import 'widgets/connection_status_card.dart';
import 'widgets/current_call_card.dart';
import 'widgets/dashboard_header.dart';
import 'widgets/device_info_card.dart';
import 'widgets/quick_stats_card.dart';

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final dashboard = ref.watch(dashboardProvider);

    return dashboard.when(
      loading: () => const Scaffold(
        body: Center(
          child: CircularProgressIndicator(),
        ),
      ),
      error: (error, _) => Scaffold(
        body: Center(
          child: Padding(
            padding: EdgeInsets.all(24),
            child: Text(
              "Error\n\n$error",
              textAlign: TextAlign.center,
            ),
          ),
        ),
      ),
      data: (data) {
        return Scaffold(
          backgroundColor: const Color(0xFFF8FAFC),
          appBar: AppBar(
            elevation: 0,
            backgroundColor: Colors.transparent,
            foregroundColor: const Color(0xFF0F172A),
            centerTitle: true,
            title: const Text(
              "Dashboard",
              style: TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold),
            ),
          ),
          body: SafeArea(
            child: ListView(
              padding: const EdgeInsets.all(20),
              children: [
                // ==========================================
                // HEADER
                // ==========================================

                DashboardHeader(
                  online: data.websocketConnected,
                ),

                const SizedBox(height: 20),

                // ==========================================
                // QUICK STATS
                // ==========================================

                Row(
                  children: [
                    QuickStatsCard(
                      title: "Calls Today",
                      value: "${data.callsToday}",
                      icon: Icons.call,
                      color: Colors.blue,
                    ),
                    const SizedBox(width: 16),
                    QuickStatsCard(
                      title: "Active",
                      value: "${data.activeCalls}",
                      icon: Icons.phone_in_talk,
                      color: Colors.green,
                    ),
                  ],
                ),

                const SizedBox(height: 16),

                Row(
                  children: [
                    QuickStatsCard(
                      title: "Total Leads",
                      value: "${data.totalLeads}",
                      icon: Icons.people,
                      color: Colors.deepPurple,
                    ),
                    const SizedBox(width: 16),
                    QuickStatsCard(
                      title: "Avg Time",
                      value: data.avgDuration,
                      icon: Icons.timer,
                      color: Colors.orange,
                    ),
                  ],
                ),

                const SizedBox(height: 24),

                // ==========================================
                // DEVICE INFORMATION
                // ==========================================

                DeviceInfoCard(
                  deviceName: data.deviceName,
                  deviceId: data.deviceId,
                  phoneNumber: data.phoneNumber,
                ),

                const SizedBox(height: 20),

                // ==========================================
                // CONNECTION STATUS
                // ==========================================

                ConnectionStatusCard(
                  backendConnected: data.backendConnected,
                  websocketConnected: data.websocketConnected,
                ),

                const SizedBox(height: 20),

                // ==========================================
                // CURRENT CALL
                // ==========================================

                CurrentCallCard(
                  status: data.currentCallStatus,
                ),

                const SizedBox(height: 20),

                // ==========================================
                // APPLICATION
                // ==========================================

                ApplicationCard(
                  version: data.appVersion,
                ),

                const SizedBox(height: 40),
              ],
            ),
          ),
        );
      },
    );
  }
}