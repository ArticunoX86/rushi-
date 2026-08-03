class ApiRoutes {
  ApiRoutes._();

  // ---------------------------------------------------------------------------
  // Authentication
  // ---------------------------------------------------------------------------

  static const String login = "/auth/login";

  static const String register = "/auth/register";

  static const String currentUser = "/auth/me";

  // ---------------------------------------------------------------------------
  // Devices
  // ---------------------------------------------------------------------------

  static const String registerDevice =
      "/devices/register";

  static const String deviceStatus =
      "/devices/status";

  // ---------------------------------------------------------------------------
  // Calls
  // ---------------------------------------------------------------------------

  static const String pendingCalls =
      "/calls/pending";

  static String acceptCall(String id) =>
      "/calls/$id/accept";

  static String rejectCall(String id) =>
      "/calls/$id/reject";

  static String completeCall(String id) =>
      "/calls/$id/complete";

  // ---------------------------------------------------------------------------
  // WebSocket
  // ---------------------------------------------------------------------------

  static const String websocket =
      "/device/connect";
}