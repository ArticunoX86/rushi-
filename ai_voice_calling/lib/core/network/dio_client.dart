import 'dart:async';
import 'package:dio/dio.dart';

import '../config/app_config.dart';

class DioClient {
  DioClient._() {
    dio.interceptors.add(
      InterceptorsWrapper(
        onError: (DioException e, handler) {
          if (e.type == DioExceptionType.connectionTimeout ||
              e.type == DioExceptionType.connectionError ||
              e.type == DioExceptionType.receiveTimeout) {
            _networkStatusController.add(true); // emit offline
          }
          return handler.next(e);
        },
        onResponse: (response, handler) {
          _networkStatusController.add(false); // emit online
          return handler.next(response);
        },
      ),
    );
  }

  static final DioClient instance = DioClient._();

  final StreamController<bool> _networkStatusController = StreamController<bool>.broadcast();
  Stream<bool> get onNetworkStatusChanged => _networkStatusController.stream;

  late final Dio dio = Dio(
    BaseOptions(
      baseUrl: AppConfig.baseUrl,
      connectTimeout: const Duration(seconds: 10), // reduced from 30s
      receiveTimeout: const Duration(seconds: 10),
      sendTimeout: const Duration(seconds: 10),
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
      },
    ),
  );
}