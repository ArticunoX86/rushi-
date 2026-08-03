import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../../../core/network/dio_client.dart';

class TranscriptsScreen extends StatefulWidget {
  const TranscriptsScreen({super.key});

  @override
  State<TranscriptsScreen> createState() => _TranscriptsScreenState();
}

class _TranscriptsScreenState extends State<TranscriptsScreen> {
  bool _isLoading = true;
  List<dynamic> _calls = [];
  String _searchQuery = "";
  String _selectedFilter = "All";
  String _dateMode = "Today"; // "Today", "Yesterday", "All Days", "Custom"
  DateTime _selectedDate = DateTime.now();
  Timer? _autoRefreshTimer;

  @override
  void initState() {
    super.initState();
    _fetchCalls();
    // Auto-refresh transcripts every 3 seconds for live streaming updates
    _autoRefreshTimer = Timer.periodic(const Duration(seconds: 3), (_) {
      if (mounted) _fetchCalls();
    });
  }

  @override
  void dispose() {
    _autoRefreshTimer?.cancel();
    super.dispose();
  }

  Future<void> _fetchCalls() async {
    try {
      final response = await DioClient.instance.dio.get('/calls/');
      if (response.statusCode == 200 && response.data != null) {
        setState(() {
          _calls = response.data;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  List<dynamic> get _filteredCalls {
    final filtered = _calls.where((call) {
      // 1. Date Filter (Only corresponding day's transcripts)
      if (_dateMode != "All Days" && call['created_at'] != null) {
        try {
          final createdAt = DateTime.parse(call['created_at'].toString()).toLocal();
          final targetDate = _dateMode == "Yesterday"
              ? DateTime.now().subtract(const Duration(days: 1))
              : _selectedDate;
          final sameDay = createdAt.year == targetDate.year &&
              createdAt.month == targetDate.month &&
              createdAt.day == targetDate.day;
          if (!sameDay) return false;
        } catch (_) {}
      }

      // 2. Keyword Search & Outcome Filter
      final summary = (call['summary'] ?? '').toString().toLowerCase();
      final transcript = (call['transcript'] ?? '').toString().toLowerCase();
      final outcome = (call['outcome'] ?? '').toString().toUpperCase();
      final query = _searchQuery.toLowerCase();

      final matchesQuery = summary.contains(query) || transcript.contains(query);
      if (_selectedFilter == "All") return matchesQuery;
      return matchesQuery && outcome.contains(_selectedFilter.toUpperCase());
    }).toList();

    // Sort: Recent call comes first
    filtered.sort((a, b) {
      final aTime = DateTime.tryParse(a['created_at']?.toString() ?? '') ?? DateTime(1970);
      final bTime = DateTime.tryParse(b['created_at']?.toString() ?? '') ?? DateTime(1970);
      return bTime.compareTo(aTime);
    });

    return filtered;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
        title: const Text(
          "Call Recordings & Transcripts",
          style: TextStyle(
            color: Color(0xFF0F172A),
            fontWeight: FontWeight.bold,
            fontSize: 18,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh, color: Color(0xFF1B8B4B)),
            onPressed: () {
              setState(() => _isLoading = true);
              _fetchCalls();
            },
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            // ==========================================
            // DATE FILTER BAR (CORRESPONDING DAY)
            // ==========================================
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 6),
              child: Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                  boxShadow: const [
                    BoxShadow(color: Colors.black12, blurRadius: 6, offset: Offset(0, 2)),
                  ],
                ),
                child: Row(
                  children: [
                    const Icon(Icons.calendar_today, color: Color(0xFF1B8B4B), size: 18),
                    const SizedBox(width: 8),
                    Expanded(
                      child: SingleChildScrollView(
                        scrollDirection: Axis.horizontal,
                        child: Row(
                          children: ["Today", "Yesterday", "All Days", "Custom Date"].map((mode) {
                            final isSel = _dateMode == mode;
                            return Padding(
                              padding: const EdgeInsets.only(right: 6),
                              child: InkWell(
                                onTap: () async {
                                  if (mode == "Custom Date") {
                                    final picked = await showDatePicker(
                                      context: context,
                                      initialDate: _selectedDate,
                                      firstDate: DateTime(2025),
                                      lastDate: DateTime(2030),
                                    );
                                    if (picked != null) {
                                      setState(() {
                                        _selectedDate = picked;
                                        _dateMode = "Custom Date";
                                      });
                                    }
                                  } else {
                                    setState(() {
                                      _dateMode = mode;
                                      if (mode == "Today") _selectedDate = DateTime.now();
                                    });
                                  }
                                },
                                child: Container(
                                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                  decoration: BoxDecoration(
                                    color: isSel ? Color(0xFF1B8B4B) : Colors.grey.shade100,
                                    borderRadius: BorderRadius.circular(10),
                                  ),
                                  child: Text(
                                    mode == "Custom Date" && _dateMode == "Custom Date"
                                        ? "${_selectedDate.day}/${_selectedDate.month}/${_selectedDate.year}"
                                        : mode,
                                    style: TextStyle(
                                      color: isSel ? Colors.white : Colors.grey.shade700,
                                      fontWeight: isSel ? FontWeight.bold : FontWeight.normal,
                                      fontSize: 12,
                                    ),
                                  ),
                                ),
                              ),
                            );
                          }).toList(),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),

            // ==========================================
            // SEARCH & FILTER BAR
            // ==========================================
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 6),
              child: TextField(
                style: const TextStyle(color: Color(0xFF0F172A)),
                decoration: InputDecoration(
                  hintText: "Search transcripts or keywords...",
                  hintStyle: TextStyle(color: Colors.grey.shade500),
                  prefixIcon: const Icon(Icons.search, color: Color(0xFF1B8B4B)),
                  filled: true,
                  fillColor: Colors.white,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(16),
                    borderSide: BorderSide(color: Colors.grey.shade300),
                  ),
                ),
                onChanged: (val) => setState(() => _searchQuery = val),
              ),
            ),

            // Filter Chips
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Row(
                children: ["All", "Interested", "Converted", "Callback"].map((filter) {
                  final isSelected = _selectedFilter == filter;
                  return Padding(
                    padding: const EdgeInsets.only(right: 8),
                    child: ChoiceChip(
                      label: Text(filter),
                      selected: isSelected,
                      selectedColor: Color(0xFF1B8B4B),
                      backgroundColor: Colors.white,
                      labelStyle: TextStyle(
                        color: isSelected ? Colors.white : Colors.grey.shade700,
                        fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                      ),
                      onSelected: (val) {
                        if (val) setState(() => _selectedFilter = filter);
                      },
                    ),
                  );
                }).toList(),
              ),
            ),

            const SizedBox(height: 10),

            // ==========================================
            // CALL LIST & TRANSCRIPTS
            // ==========================================
            Expanded(
              child: _isLoading
                  ? const Center(child: CircularProgressIndicator(color: Color(0xFF1B8B4B)))
                  : _filteredCalls.isEmpty
                      ? _buildEmptyState()
                      : ListView.builder(
                          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                          itemCount: _filteredCalls.length,
                          itemBuilder: (context, index) {
                            final call = _filteredCalls[index];
                            return _buildTranscriptCard(call);
                          },
                        ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.mic_none, size: 48, color: Colors.grey.shade400),
          const SizedBox(height: 12),
          Text(
            "No Call Recordings Found",
            style: TextStyle(color: Colors.grey.shade700, fontSize: 16, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 4),
          Text(
            "Completed AI calls will stream live transcripts & audio recordings here.",
            style: TextStyle(color: Colors.grey.shade500, fontSize: 12),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Widget _buildTranscriptCard(Map<String, dynamic> call) {
    final String callId = (call['id'] ?? '').toString();
    final String outcome = (call['outcome'] ?? 'COMPLETED').toString().toUpperCase();
    final int duration = call['duration_seconds'] ?? 0;
    final String durationStr = "${duration ~/ 60}:${(duration % 60).toString().padLeft(2, '0')}";
    final String summary = call['summary'] ?? "AI Lead Qualification Call Completed.";
    final String transcript = call['transcript'] ?? "Assistant: Hello! Calling regarding your real estate inquiry.\nCustomer: Yes, I am interested in a 2 BHK apartment.";
    final String? recordingUrl = call['recording_url'];

    final Color badgeColor = outcome.contains("INTERESTED") || outcome.contains("CONVERTED")
        ? Colors.green
        : outcome.contains("CALLBACK")
            ? Colors.amber.shade800
            : Color(0xFF1B8B4B);

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: const [
          BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 3)),
        ],
        border: Border.all(color: badgeColor.withOpacity(0.3), width: 1),
      ),
      child: Material(
        color: Colors.transparent,
        borderRadius: BorderRadius.circular(20),
        child: ExpansionTile(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
          collapsedShape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
          tilePadding: const EdgeInsets.symmetric(horizontal: 18, vertical: 8),
        iconColor: Color(0xFF1B8B4B),
        collapsedIconColor: Colors.grey.shade600,
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: badgeColor.withOpacity(0.12),
                shape: BoxShape.circle,
              ),
              child: Icon(Icons.record_voice_over, color: badgeColor, size: 20),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "Call ${callId.length > 8 ? callId.substring(0, 8) : callId}",
                    style: const TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold, fontSize: 15),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    "Duration: $durationStr",
                    style: TextStyle(color: Colors.grey.shade600, fontSize: 12),
                  ),
                ],
              ),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(
                color: badgeColor.withOpacity(0.12),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Text(
                outcome,
                style: TextStyle(color: badgeColor, fontSize: 11, fontWeight: FontWeight.bold),
              ),
            ),
          ],
        ),
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Divider(color: Colors.grey.shade300),
                const SizedBox(height: 6),

                // AI Executive Summary
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF8FAFC),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Color(0xFF1B8B4B).withOpacity(0.3)),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: const [
                          Icon(Icons.auto_awesome, color: Color(0xFF1B8B4B), size: 16),
                          SizedBox(width: 6),
                          Text("AI Call Summary", style: TextStyle(color: Color(0xFF1B8B4B), fontWeight: FontWeight.bold, fontSize: 12)),
                        ],
                      ),
                      const SizedBox(height: 6),
                      Text(summary, style: TextStyle(color: Colors.grey.shade800, fontSize: 13)),
                    ],
                  ),
                ),

                const SizedBox(height: 14),

                // AWS S3 Recording Player Button
                if (recordingUrl != null && recordingUrl.isNotEmpty) ...[
                  ElevatedButton.icon(
                    onPressed: () {
                      Clipboard.setData(ClipboardData(text: recordingUrl));
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text("AWS S3 Recording URL copied to clipboard!")),
                      );
                    },
                    icon: const Icon(Icons.play_circle_fill, color: Colors.white, size: 18),
                    label: const Text("Copy S3 Audio Recording Link"),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Color(0xFF1B8B4B),
                      foregroundColor: Colors.white,
                      minimumSize: const Size.fromHeight(40),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                  ),
                  const SizedBox(height: 14),
                ],

                // Full Transcript
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text("Full Conversation Transcript", style: TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold, fontSize: 13)),
                    IconButton(
                      icon: Icon(Icons.copy, color: Colors.grey.shade600, size: 18),
                      onPressed: () {
                        Clipboard.setData(ClipboardData(text: transcript));
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text("Transcript copied to clipboard!")),
                        );
                      },
                    ),
                  ],
                ),
                const SizedBox(height: 6),

                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF8FAFC),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.grey.shade300),
                  ),
                  child: Text(
                    transcript,
                    style: const TextStyle(color: Color(0xFF0F172A), fontFamily: 'monospace', fontSize: 12, height: 1.4),
                  ),
                ),
                const SizedBox(height: 10),
              ],
            ),
          ),
        ],
      ),
    ),
    );
  }
}
