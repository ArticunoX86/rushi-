class DashboardInfo {
  final String deviceName;
  final String deviceId;
  final String phoneNumber;
  final String appVersion;
  final bool backendConnected;
  final bool websocketConnected;
  final String currentCallStatus;

  // Real-time backend stats
  final int callsToday;
  final int activeCalls;
  final int completedCalls;
  final String avgDuration;
  final int totalLeads;
  final double conversionRatePct;

  const DashboardInfo({
    required this.deviceName,
    required this.deviceId,
    required this.phoneNumber,
    required this.appVersion,
    required this.backendConnected,
    required this.websocketConnected,
    required this.currentCallStatus,
    this.callsToday = 0,
    this.activeCalls = 0,
    this.completedCalls = 0,
    this.avgDuration = "00:00",
    this.totalLeads = 0,
    this.conversionRatePct = 0.0,
  });
}