import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/app_config.dart';
import '../device/device_service.dart';
import 'app_logger.dart';

class BackendLogService {
  BackendLogService._();

  static final BackendLogService instance = BackendLogService._();

  bool _isSyncing = false;

  Future<void> syncLogs(List<String> logs) async {
    if (logs.isEmpty) return;
    if (_isSyncing) return;

    _isSyncing = true;
    try {
      final deviceInfo = await DeviceService.instance.getDeviceInfo();
      final deviceId = deviceInfo['device_identifier'] ?? 'unknown_device';

      final logEntries = logs.map((log) {
        String level = "INFO";
        if (log.contains("❌") || log.contains("ERROR") || log.contains("failed") || log.contains("Exception")) {
          level = "ERROR";
        } else if (log.contains("⚠️") || log.contains("Warning") || log.contains("warn")) {
          level = "WARNING";
        }
        return {
          "log_level": level,
          "message": log,
          "timestamp": DateTime.now().toIso8601String(),
        };
      }).toList();

      final response = await http.post(
        Uri.parse("${AppConfig.baseUrl}/logs/batch"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "device_identifier": deviceId,
          "logs": logEntries,
        }),
      );

      if (response.statusCode != 201) {
        AppLogger.logger.e("Failed to sync logs: ${response.statusCode} - ${response.body}");
      }
    } catch (e) {
      AppLogger.logger.w("Log sync retry pending (backend reconnecting): ${e.toString()}");
    } finally {
      _isSyncing = false;
    }
  }
}
