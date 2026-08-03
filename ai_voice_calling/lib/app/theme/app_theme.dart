import 'package:flutter/material.dart';

class AppTheme {
  AppTheme._();

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,

      brightness: Brightness.light,

      colorScheme: ColorScheme.fromSeed(
        seedColor: const Color(0xFF1B8B4B),
        brightness: Brightness.light,
      ),

      scaffoldBackgroundColor: const Color(0xFFF4F7F5),

      appBarTheme: const AppBarTheme(
        elevation: 0,
        centerTitle: true,
        backgroundColor: Colors.transparent,
        foregroundColor: Color(0xFF1C1C2E),
        surfaceTintColor: Colors.transparent,
      ),

      cardTheme: CardThemeData(
        elevation: 2,
        color: Colors.white,
        surfaceTintColor: Colors.transparent,
        shadowColor: Colors.black12,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
      ),

      dividerTheme: const DividerThemeData(
        thickness: 1,
        color: Color(0xFFE5E7EB),
      ),

      textTheme: const TextTheme(
        headlineMedium: TextStyle(
          fontSize: 28,
          fontWeight: FontWeight.bold,
          color: Color(0xFF1C1C2E),
        ),
        titleLarge: TextStyle(
          fontSize: 20,
          fontWeight: FontWeight.bold,
          color: Color(0xFF1C1C2E),
        ),
        bodyLarge: TextStyle(
          fontSize: 16,
          color: Color(0xFF1C1C2E),
        ),
        bodyMedium: TextStyle(
          fontSize: 14,
          color: Color(0xFF6B7280),
        ),
      ),
    );
  }
}