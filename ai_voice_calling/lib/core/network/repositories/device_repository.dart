import 'package:dio/dio.dart';

import '../../device/device_service.dart';
import '../dio_client.dart';

class DeviceRepository {
  DeviceRepository._();

  static final DeviceRepository instance = DeviceRepository._();

  final Dio _dio = DioClient.instance.dio;

  Future<void> registerDevice() async {
    final device = await DeviceService.instance.getDeviceInfo();

    final payload = {
      "device_name": device["device_name"],
      "device_identifier": device["device_id"],
      "phone_number": null,
    };

    final response = await _dio.post(
      "/devices/register",
      data: payload,
    );

    print("======================================");
    print("DEVICE REGISTERED");
    print(response.data);
    print("======================================");
  }
}