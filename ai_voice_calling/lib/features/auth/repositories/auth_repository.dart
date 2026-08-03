import 'package:dio/dio.dart';

import '../../../core/network/dio_client.dart';
import '../models/auth_response.dart';
import '../models/login_request.dart';

class AuthRepository {
  AuthRepository._();

  static final AuthRepository instance = AuthRepository._();

  final Dio _dio = DioClient.instance.dio;

  Future<AuthResponse> login(
    LoginRequest request,
  ) async {
    final response = await _dio.post(
      "/auth/login",
      data: {
        "username": request.email,
        "password": request.password,
      },
      options: Options(
        contentType: Headers.formUrlEncodedContentType,
      ),
    );

    return AuthResponse.fromJson(
      response.data,
    );
  }
}