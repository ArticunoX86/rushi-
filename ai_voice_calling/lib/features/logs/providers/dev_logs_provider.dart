import 'dart:async';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../../core/logger/app_logger.dart';
import '../../../core/logger/backend_log_service.dart';

final devLogsProvider = StateNotifierProvider<DevLogsNotifier, List<String>>((ref) {
  final notifier = DevLogsNotifier();
  notifier.loadLogsAndListen();
  ref.onDispose(() => notifier.disposeSubscription());
  return notifier;
});

class DevLogsNotifier extends StateNotifier<List<String>> {
  DevLogsNotifier() : super([]);

  StreamSubscription? _subscription;
  Timer? _syncTimer;
  final List<String> _unSyncedLogs = [];
  static const String _prefKey = "dev_console_logs";

  Future<void> loadLogsAndListen() async {
    final prefs = await SharedPreferences.getInstance();
    final savedLogs = prefs.getStringList(_prefKey) ?? [];
    state = savedLogs;

    _subscription?.cancel();
    _subscription = AppLogger.logStream.listen((logLine) async {
      final currentList = state;
      List<String> newList;
      if (currentList.length >= 1000) {
        newList = [...currentList.sublist(currentList.length - 999), logLine];
      } else {
        newList = [...currentList, logLine];
      }
      state = newList;

      final prefsInstance = await SharedPreferences.getInstance();
      await prefsInstance.setStringList(_prefKey, newList);

      _unSyncedLogs.add(logLine);
    });

    _syncTimer?.cancel();
    _syncTimer = Timer.periodic(const Duration(seconds: 10), (_) {
      _syncLogsToBackend();
    });
  }

  void _syncLogsToBackend() {
    if (_unSyncedLogs.isEmpty) return;
    
    final logsToSync = List<String>.from(_unSyncedLogs);
    _unSyncedLogs.clear();

    BackendLogService.instance.syncLogs(logsToSync).catchError((_) {
      // If sync fails, put them back (basic retry mechanism)
      _unSyncedLogs.insertAll(0, logsToSync);
    });
  }

  Future<void> clearLogs() async {
    state = [];
    _unSyncedLogs.clear();
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_prefKey);
  }

  void disposeSubscription() {
    _subscription?.cancel();
  }
}
