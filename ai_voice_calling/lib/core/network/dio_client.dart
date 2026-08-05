import 'dart:async';
import 'package:dio/dio.dart';

import '../config/app_config.dart';

class DioClient {
  DioClient._() {
    dio.interceptors.add(
      InterceptorsWrapper(
        onError: (DioException e, handler) async {
          if (_isTransientError(e)) {
            _networkStatusController.add(true); // emit offline
            
            // Implement Exponential Backoff Retry (Max 3 retries)
            final extra = e.requestOptions.extra;
            final int retries = (extra['retries'] as int?) ?? 0;
            if (retries < 3) {
              extra['retries'] = retries + 1;
              await Future.delayed(Duration(milliseconds: 1000 * (retries + 1)));
              try {
                final response = await dio.fetch(e.requestOptions);
                return handler.resolve(response);
              } catch (retryError) {
                if (retryError is DioException) {
                  return handler.next(retryError);
                }
              }
            }
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

  bool _isTransientError(DioException e) {
    return e.type == DioExceptionType.connectionTimeout ||
           e.type == DioExceptionType.connectionError ||
           e.type == DioExceptionType.receiveTimeout ||
           (e.response != null && e.response!.statusCode! >= 500);
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