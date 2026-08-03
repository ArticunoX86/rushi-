import 'package:dio/dio.dart';

import '../../../core/network/dio_client.dart';
import '../models/call_job.dart';

class CallService {
  CallService._();

  static final CallService instance = CallService._();

  final Dio _dio = DioClient.instance.dio;

  Future<List<CallJob>> fetchPendingCalls() async {
    final response = await _dio.get(
      "/calls/pending",
    );

    final List<dynamic> data = response.data;

    return data
        .map(
          (json) => CallJob.fromJson(json),
        )
        .toList();
  }

  Future<void> acceptCall(
    String callId,
  ) async {
    await _dio.post(
      "/calls/$callId/accept",
    );
  }

  Future<void> rejectCall(
    String callId,
  ) async {
    await _dio.post(
      "/calls/$callId/reject",
    );
  }

  Future<void> completeCall(
    String callId,
  ) async {
    await _dio.post(
      "/calls/$callId/complete",
    );
  }
}