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

  // AWS CONFIG (Raw IP since no Domain is used)
  // Replace this with your actual AWS Public IPv4 Address after launching EC2
  static const String _awsHost = "43.205.19.246";
  static const int _awsPort = 8000;

  static String get backendHost => isProduction ? _awsHost : _localHost;
  static int get backendPort => isProduction ? _awsPort : _localPort;

  // Since we are using Raw IP (No SSL Domain), we use http:// and ws://
  static String get baseUrl => "http://$backendHost:$backendPort";
  static String get websocketUrl => "ws://$backendHost:$backendPort";
}