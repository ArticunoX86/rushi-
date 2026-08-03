import 'package:device_info_plus/device_info_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:uuid/uuid.dart';

class DeviceService {
  DeviceService._();

  static final DeviceService instance = DeviceService._();

  static const _deviceIdKey = "device_id";

  final DeviceInfoPlugin _deviceInfo = DeviceInfoPlugin();

  final Uuid _uuid = const Uuid();

  // ==========================================================
  // DEVICE ID
  // ==========================================================

  Future<String> getDeviceId() async {
    final prefs = await SharedPreferences.getInstance();

    final existingId = prefs.getString(_deviceIdKey);

    if (existingId != null) {
      return existingId;
    }

    final newId = _uuid.v4();

    await prefs.setString(
      _deviceIdKey,
      newId,
    );

    return newId;
  }

  // ==========================================================
  // DEVICE NAME
  // ==========================================================

  Future<String> getDeviceName() async {
    final info = await _deviceInfo.androidInfo;

    return "${info.manufacturer} ${info.model}";
  }

  // ==========================================================
  // DEVICE MODEL
  // ==========================================================

  Future<String> getModel() async {
    final info = await _deviceInfo.androidInfo;

    return info.model;
  }

  // ==========================================================
  // ANDROID VERSION
  // ==========================================================

  Future<String> getAndroidVersion() async {
    final info = await _deviceInfo.androidInfo;

    return info.version.release;
  }

  // ==========================================================
  // SDK VERSION
  // ==========================================================

  Future<int> getSdkVersion() async {
    final info = await _deviceInfo.androidInfo;

    return info.version.sdkInt;
  }
}