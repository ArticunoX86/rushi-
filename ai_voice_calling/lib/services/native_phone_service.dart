import 'package:flutter/services.dart';

class NativePhoneService {
  static const MethodChannel _channel =
      MethodChannel('ai_voice_calling/phone');

  static Future<void> makeCall(
    String phoneNumber,
  ) async {
    await _channel.invokeMethod(
      "makeCall",
      {
        "phoneNumber": phoneNumber,
      },
    );
  }
}