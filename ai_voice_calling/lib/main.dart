import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'app/app.dart';
import 'core/device/device_service.dart';
import 'services/call_state_service.dart';
import 'core/logger/app_logger.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  FlutterError.onError = (details) {
    AppLogger.logger.e(
      "Unhandled Flutter Error: ${details.exception}",
      error: details.exception,
      stackTrace: details.stack,
    );
  };

  PlatformDispatcher.instance.onError = (error, stack) {
    AppLogger.logger.e(
      "Unhandled Async Error: $error",
      error: error,
      stackTrace: stack,
    );
    return true;
  };

  final deviceInfo =
      await DeviceService.instance.getDeviceInfo();

  AppLogger.logger.i("==================================");
  AppLogger.logger.i("DEVICE INFO");
  AppLogger.logger.i(deviceInfo.toString());
  AppLogger.logger.i("==================================");

  AppLogger.logger.i("Starting CallStateService...");

  CallStateService.instance.startListening();

  AppLogger.logger.i("CallStateService Started.");

  runApp(
    const ProviderScope(
      child: AIVoiceCallingApp(),
    ),
  );
}