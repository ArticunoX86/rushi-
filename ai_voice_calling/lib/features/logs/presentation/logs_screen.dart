import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/dev_logs_provider.dart';

class LogsScreen extends ConsumerStatefulWidget {
  const LogsScreen({super.key});

  @override
  ConsumerState<LogsScreen> createState() => _LogsScreenState();
}

class _LogsScreenState extends ConsumerState<LogsScreen> {
  final ScrollController _scrollController = ScrollController();
  final TextEditingController _searchController = TextEditingController();
  String _filterQuery = "";
  bool _autoScroll = true;

  @override
  void initState() {
    super.initState();
    _searchController.addListener(() {
      setState(() {
        _filterQuery = _searchController.text.toLowerCase();
      });
    });
  }

  @override
  void dispose() {
    _scrollController.dispose();
    _searchController.dispose();
    super.dispose();
  }

  void _scrollToBottom() {
    if (_autoScroll && _scrollController.hasClients) {
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: const Duration(milliseconds: 200),
        curve: Curves.easeOut,
      );
    }
  }

  Color _getLineColor(String line) {
    if (line.contains("❌") || line.contains("ERROR") || line.contains("failed")) {
      return Colors.redAccent;
    }
    if (line.contains("⚠️") || line.contains("Warning") || line.contains("warn")) {
      return Colors.amberAccent;
    }
    if (line.contains("📞") || line.contains("CALL") || line.contains("State")) {
      return Colors.cyanAccent;
    }
    if (line.contains("SUCCESS") || line.contains("Connected")) {
      return Colors.greenAccent;
    }
    return Colors.white70;
  }

  @override
  Widget build(BuildContext context) {
    final rawLogs = ref.watch(devLogsProvider);
    final logs = rawLogs.where((line) => line.toLowerCase().contains(_filterQuery)).toList();

    // Trigger auto-scroll when new logs arrive
    WidgetsBinding.instance.addPostFrameCallback((_) => _scrollToBottom());

    return Scaffold(
      backgroundColor: const Color(0xFF0F172A), // Premium dark theme
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        title: const Text(
          "Developer Console Logs",
          style: TextStyle(
            color: Colors.white,
            fontFamily: 'monospace',
            fontSize: 18,
          ),
        ),
        actions: [
          IconButton(
            tooltip: "Copy all logs",
            icon: const Icon(Icons.copy, color: Colors.white70),
            onPressed: () {
              Clipboard.setData(ClipboardData(text: rawLogs.join('\n')));
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text("Logs copied to clipboard")),
              );
            },
          ),
          IconButton(
            tooltip: "Clear Logs",
            icon: const Icon(Icons.delete_sweep, color: Colors.redAccent),
            onPressed: () {
              ref.read(devLogsProvider.notifier).clearLogs();
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // Search & Filters Panel
          Container(
            color: const Color(0xFF1E293B),
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _searchController,
                    style: const TextStyle(color: Colors.white, fontFamily: 'monospace'),
                    decoration: InputDecoration(
                      hintText: "Filter logs...",
                      hintStyle: const TextStyle(color: Colors.white38),
                      prefixIcon: const Icon(Icons.search, color: Colors.white54),
                      fillColor: const Color(0xFF0F172A),
                      filled: true,
                      contentPadding: const EdgeInsets.symmetric(vertical: 0, horizontal: 16),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: BorderSide.none,
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  tooltip: _autoScroll ? "Disable Auto-scroll" : "Enable Auto-scroll",
                  icon: Icon(
                    _autoScroll ? Icons.arrow_downward : Icons.vertical_align_bottom,
                    color: _autoScroll ? Colors.greenAccent : Colors.white38,
                  ),
                  onPressed: () {
                    setState(() {
                      _autoScroll = !_autoScroll;
                    });
                  },
                )
              ],
            ),
          ),
          // Log output terminal
          Expanded(
            child: Container(
              margin: const EdgeInsets.all(8),
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: const Color(0xFF020617), // Deeper black terminal screen
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: const Color(0xFF334155)),
              ),
              child: logs.isEmpty
                  ? const Center(
                      child: Text(
                        "No logs captured yet.",
                        style: TextStyle(color: Colors.white38, fontFamily: 'monospace'),
                      ),
                    )
                  : ListView.builder(
                      controller: _scrollController,
                      itemCount: logs.length,
                      itemBuilder: (context, index) {
                        final line = logs[index];
                        return Padding(
                          padding: const EdgeInsets.symmetric(vertical: 2.0),
                          child: Text(
                            line,
                            style: TextStyle(
                              color: _getLineColor(line),
                              fontFamily: 'monospace',
                              fontSize: 12,
                              height: 1.3,
                            ),
                          ),
                        );
                      },
                    ),
            ),
          ),
        ],
      ),
    );
  }
}
