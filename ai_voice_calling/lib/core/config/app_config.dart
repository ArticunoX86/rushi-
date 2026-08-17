class AppConfig {
  AppConfig._();

  static const String appName = "AI Voice Calling";
  static const String appVersion = "1.0.0";

  // ==========================================
  // DEPLOYMENT CONFIGURATION
  // ==========================================
  // Set to TRUE when compiling the APK for production (AWS)
  static const bool isProduction = true; 

  // LOCAL CONFIG (Testing on Wi-Fi)
  static const String _localHost = "192.168.1.9";
  static const int _localPort = 8000;

  // AWS CONFIG (With SSL Domain and Nginx Proxy)
  static const String _awsHost = "43.205.19.246.nip.io";

  static String get backendHost => isProduction ? _awsHost : _localHost;

  static String get baseUrl => isProduction ? "https://$_awsHost/api" : "http://$_localHost:8000";
  static String get websocketUrl => isProduction ? "wss://$_awsHost/api" : "ws://$_localHost:8000";
}