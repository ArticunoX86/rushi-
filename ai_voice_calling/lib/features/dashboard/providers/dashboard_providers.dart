import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/device/device_service.dart';
import '../../../core/network/dio_client.dart';
import '../../../core/network/websocket_provider.dart';
import '../../../core/network/websocket_state.dart';
import '../models/dashboard_info.dart';

final dashboardProvider = FutureProvider<DashboardInfo>((ref) async {
  final deviceInfo = await DeviceService.instance.getDeviceInfo();
  final websocketState = ref.watch(websocketProvider);

  int callsToday = 0;
  int activeCalls = 0;
  int completedCalls = 0;
  String avgDuration = "00:00";
  int totalLeads = 0;
  double conversionRatePct = 0.0;

  try {
    final response = await DioClient.instance.dio.get('/dashboard/stats');
    if (response.statusCode == 200 && response.data != null) {
      final data = response.data['data'];
      callsToday = data['calls_today'] ?? 0;
      activeCalls = data['active_calls'] ?? 0;
      completedCalls = data['completed_calls'] ?? 0;
      avgDuration = data['avg_duration'] ?? "00:00";
      totalLeads = data['total_leads'] ?? 0;
      conversionRatePct = (data['conversion_rate_pct'] ?? 0.0).toDouble();
    }
  } catch (e) {
    // Fallback if backend stats fails
  }

  return DashboardInfo(
    deviceName: deviceInfo["device_name"] ?? "Unknown Device",
    deviceId: deviceInfo["device_id"] ?? "Unknown",
    phoneNumber: deviceInfo["phone_number"] ?? "Not Assigned",
    appVersion: "1.0.0",
    backendConnected: websocketState.status == WebSocketStatus.connected,
    websocketConnected: websocketState.status == WebSocketStatus.connected,
    currentCallStatus: activeCalls > 0 ? "Call Active" : "Idle",
    callsToday: callsToday,
    activeCalls: activeCalls,
    completedCalls: completedCalls,
    avgDuration: avgDuration,
    totalLeads: totalLeads,
    conversionRatePct: conversionRatePct,
  );
});