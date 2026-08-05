import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import '../logger/app_logger.dart';

class GlobalErrorHandler {
  static final GlobalKey<ScaffoldMessengerState> scaffoldMessengerKey = GlobalKey<ScaffoldMessengerState>();

  static void handleError(dynamic error, {String? customMessage}) {
    AppLogger.logger.e("GlobalErrorHandler caught: $error");

    String displayMessage = customMessage ?? "An unexpected error occurred. Please try again.";

    if (error is DioException) {
      if (error.type == DioExceptionType.connectionTimeout || 
          error.type == DioExceptionType.connectionError ||
          error.type == DioExceptionType.receiveTimeout) {
        displayMessage = "Network error. Please check your connection.";
      } else if (error.response != null) {
        displayMessage = "Server error (${error.response!.statusCode}). Please try again later.";
      }
    }

    _showErrorSnackBar(displayMessage);
  }

  static void _showErrorSnackBar(String message) {
    if (scaffoldMessengerKey.currentState != null) {
      scaffoldMessengerKey.currentState!.showSnackBar(
        SnackBar(
          content: Row(
            children: [
              const Icon(Icons.error_outline, color: Colors.white, size: 20),
              const SizedBox(width: 10),
              Expanded(child: Text(message, style: const TextStyle(color: Colors.white))),
            ],
          ),
          backgroundColor: Colors.redAccent.shade700,
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
          margin: const EdgeInsets.all(16),
          duration: const Duration(seconds: 4),
        ),
      );
    }
  }
}
