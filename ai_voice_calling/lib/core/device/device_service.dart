import 'package:device_info_plus/device_info_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:uuid/uuid.dart';

class DeviceService {
  DeviceService._();

  static final DeviceService instance = DeviceService._();

  static const String _deviceIdKey = "device_id";

  final DeviceInfoPlugin _deviceInfo = DeviceInfoPlugin();

  final Uuid _uuid = const Uuid();

  // =====================================================
  // DEVICE ID
  // =====================================================

  Future<String> getDeviceId() async {
    final prefs = await SharedPreferences.getInstance();

    final savedId = prefs.getString(_deviceIdKey);

    if (savedId != null) {
      return savedId;
    }

    final newId = _uuid.v4();

    await prefs.setString(
      _deviceIdKey,
      newId,
    );

    return newId;
  }

  // =====================================================
  // DEVICE NAME
  // =====================================================

  Future<String> getDeviceName() async {
    final info = await _deviceInfo.androidInfo;

    return "${info.manufacturer} ${info.model}";
  }

  // =====================================================
  // MODEL
  // =====================================================

  Future<String> getModel() async {
    final info = await _deviceInfo.androidInfo;

    return info.model;
  }

  // =====================================================
  // ANDROID VERSION
  // =====================================================

  Future<String> getAndroidVersion() async {
    final info = await _deviceInfo.androidInfo;

    return info.version.release;
  }

  // =====================================================
  // SDK VERSION
  // =====================================================

  Future<int> getSdkVersion() async {
    final info = await _deviceInfo.androidInfo;

    return info.version.sdkInt;
  }

  // =====================================================
  // COMPLETE DEVICE INFO
  // =====================================================

  Future<Map<String, dynamic>> getDeviceInfo() async {
    return {
      "device_id": await getDeviceId(),
      "device_name": await getDeviceName(),
      "model": await getModel(),
      "android_version": await getAndroidVersion(),
      "sdk_version": await getSdkVersion(),
      "platform": "android",
    };
  }
}