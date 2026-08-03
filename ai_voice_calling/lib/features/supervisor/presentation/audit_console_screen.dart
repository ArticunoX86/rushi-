import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/network/dio_client.dart';
import '../../../core/websocket/websocket_event_router.dart';
import '../../../core/websocket/websocket_event_type.dart';

class AuditConsoleScreen extends ConsumerStatefulWidget {
  const AuditConsoleScreen({super.key});

  @override
  ConsumerState<AuditConsoleScreen> createState() => _AuditConsoleScreenState();
}

class _AuditConsoleScreenState extends ConsumerState<AuditConsoleScreen> {
  bool _isLoading = true;
  Map<String, dynamic>? _activeCall;
  List<Map<String, String>> _liveTranscript = [];
  final TextEditingController _whisperController = TextEditingController();
  StreamSubscription? _websocketSubscription;
  Timer? _pollingTimer;

  final List<String> _quickWhispers = [
    "Offer 5% discount on booking amount",
    "Suggest Saturday 4 PM site visit",
    "Ask if they have a home loan pre-approved",
    "Pitch the Bandra 2 BHK terrace project",
  ];

  @override
  void initState() {
    super.initState();
    _checkActiveCall();
    // Periodically check for active calls every 3 seconds
    _pollingTimer = Timer.periodic(const Duration(seconds: 3), (_) {
      _checkActiveCall();
    });

    // Subscribe to live transcript broadcasts from backend
    _websocketSubscription = WebSocketEventRouter.instance.stream.listen((event) {
      if (event.type == WebSocketEventType.transcript || event.type == WebSocketEventType.callEnded) {
        _checkActiveCall();
      }
      
      // Look for our custom live transcript action broadcasted from the server
      final payload = event.payload;
      final action = payload['action'] ?? payload['event'] ?? '';
      
      if (action == "TRANSCRIPT_LIVE") {
        final data = payload['payload'] ?? payload;
        final callId = data['call_id']?.toString() ?? '';
        
        if (_activeCall != null && _activeCall!['id'] == callId) {
          final custMsg = data['customer_message']?.toString() ?? '';
          final aiMsg = data['ai_message']?.toString() ?? '';
          
          setState(() {
            if (custMsg.isNotEmpty) {
              _liveTranscript.add({"sender": "Customer", "text": custMsg});
            }
            if (aiMsg.isNotEmpty) {
              _liveTranscript.add({"sender": "AI", "text": aiMsg});
            }
          });
        }
      }
    });
  }

  @override
  void dispose() {
    _pollingTimer?.cancel();
    _websocketSubscription?.cancel();
    _whisperController.dispose();
    super.dispose();
  }

  Future<void> _checkActiveCall() async {
    try {
      final response = await DioClient.instance.dio.get('/calls/');
      if (response.statusCode == 200 && response.data != null) {
        final List<dynamic> calls = response.data;
        final active = calls.firstWhere(
          (call) => call['status']?.toString().toUpperCase() == "IN_PROGRESS",
          orElse: () => null,
        );

        if (active != null) {
          final isNewCall = _activeCall == null || _activeCall!['id'] != active['id'];
          setState(() {
            _activeCall = active;
            _isLoading = false;
            if (isNewCall) {
              _liveTranscript = [];
              // Load historical lines from backend if any
              final existingTranscript = active['transcript']?.toString() ?? '';
              if (existingTranscript.isNotEmpty) {
                final lines = existingTranscript.split('\n');
                for (var line in lines) {
                  if (line.startsWith("Customer:")) {
                    _liveTranscript.add({"sender": "Customer", "text": line.replaceFirst("Customer:", "").trim()});
                  } else if (line.startsWith("AI:")) {
                    _liveTranscript.add({"sender": "AI", "text": line.replaceFirst("AI:", "").trim()});
                  }
                }
              }
            }
          });
        } else {
          setState(() {
            _activeCall = null;
            _isLoading = false;
            _liveTranscript = [];
          });
        }
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  Future<void> _sendWhisper(String hint) async {
    if (_activeCall == null) return;
    final callId = _activeCall!['id'];
    try {
      final response = await DioClient.instance.dio.post(
        '/calls/$callId/whisper',
        data: {"hint": hint},
      );
      if (response.statusCode == 200) {
        _whisperController.clear();
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: Colors.indigo,
            content: Row(
              children: const [
                Icon(Icons.check_circle, color: Colors.white),
                SizedBox(width: 8),
                Text("Whisper instruction queued for AI!"),
              ],
            ),
          ),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Failed to inject whisper")),
      );
    }
  }

  Future<void> _takeoverCall() async {
    if (_activeCall == null) return;
    final callId = _activeCall!['id'];
    try {
      final response = await DioClient.instance.dio.post('/calls/$callId/takeover');
      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            backgroundColor: Colors.green,
            content: Text("Bridge established. Human Supervisor has taken over call!"),
          ),
        );
        _checkActiveCall();
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Failed to perform takeover")),
      );
    }
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
          "Live Auditing Console",
          style: TextStyle(
            color: Color(0xFF0F172A),
            fontWeight: FontWeight.bold,
            fontSize: 18,
          ),
        ),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator(color: Colors.blueAccent))
          : _activeCall == null
              ? _buildEmptyConsole()
              : _buildAuditingConsole(),
    );
  }

  Widget _buildEmptyConsole() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.hearing, size: 64, color: Colors.grey.shade400),
          const SizedBox(height: 16),
          const Text(
            "Console Idle — No Active Calls",
            style: TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold, fontSize: 16),
          ),
          const SizedBox(height: 6),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 40),
            child: Text(
              "When a customer accepts an AI outbound call, the supervisor console will dynamically connect to the live transcript and whisper panel.",
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.grey.shade500, fontSize: 12),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAuditingConsole() {
    final String callId = _activeCall!['id'].toString();
    final String shortId = callId.length > 8 ? callId.substring(0, 8) : callId;

    return SafeArea(
      child: Column(
        children: [
          // ==========================================
          // LIVE CALL CALL-CARD
          // ==========================================
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
            child: Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(20),
                boxShadow: const [
                  BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 3)),
                ],
                border: Border.all(color: Colors.redAccent.withOpacity(0.3), width: 1.5),
              ),
              child: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: Colors.red.withOpacity(0.12),
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.record_voice_over, color: Colors.redAccent, size: 24),
                  ),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          "Call ID: #$shortId",
                          style: const TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold, fontSize: 15),
                        ),
                        const SizedBox(height: 4),
                        Row(
                          children: [
                            Container(
                              width: 8,
                              height: 8,
                              decoration: const BoxDecoration(
                                color: Colors.redAccent,
                                shape: BoxShape.circle,
                              ),
                            ),
                            const SizedBox(width: 6),
                            const Text(
                              "LIVE CALL IN PROGRESS",
                              style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold, fontSize: 11),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),

          // ==========================================
          // LIVE TRANSCRIPT CONTAINER
          // ==========================================
          Expanded(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: Colors.grey.shade300),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: const [
                        Text(
                          "Real-time Conversation Logs",
                          style: TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold, fontSize: 13),
                        ),
                        Icon(Icons.hearing_disabled, color: Colors.blueAccent, size: 16),
                      ],
                    ),
                    const Divider(height: 20),
                    Expanded(
                      child: _liveTranscript.isEmpty
                          ? Center(
                              child: Text(
                                "Waiting for conversation turns...",
                                style: TextStyle(color: Colors.grey.shade500, fontSize: 12),
                              ),
                            )
                          : ListView.builder(
                              itemCount: _liveTranscript.length,
                              itemBuilder: (context, index) {
                                final msg = _liveTranscript[index];
                                final isAI = msg['sender'] == "AI";
                                return _buildDialogBubble(msg['text'] ?? '', isAI);
                              },
                            ),
                    ),
                  ],
                ),
              ),
            ),
          ),

          // ==========================================
          // SUPERVISOR WHISPER CONSOLE
          // ==========================================
          Padding(
            padding: const EdgeInsets.all(20),
            child: Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(20),
                boxShadow: const [
                  BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 3)),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: const [
                      Icon(Icons.campaign, color: Colors.indigoAccent, size: 18),
                      SizedBox(width: 8),
                      Text(
                        "Supervisor Whisper Hints (Injected Live to AI)",
                        style: TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold, fontSize: 12),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),

                  // Quick Action Whisper Chips
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children: _quickWhispers.map((hint) {
                        return Padding(
                          padding: const EdgeInsets.only(right: 6),
                          child: ActionChip(
                            backgroundColor: Colors.grey.shade100,
                            label: Text(
                              hint.length > 20 ? "${hint.substring(0, 20)}..." : hint,
                              style: const TextStyle(fontSize: 11, color: Colors.indigo),
                            ),
                            onPressed: () => _sendWhisper(hint),
                          ),
                        );
                      }).toList(),
                    ),
                  ),

                  const SizedBox(height: 10),

                  // Custom Whisper Entry Input
                  Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: _whisperController,
                          style: const TextStyle(fontSize: 13, color: Color(0xFF0F172A)),
                          decoration: InputDecoration(
                            hintText: "Enter supervisor instructions here...",
                            filled: true,
                            fillColor: const Color(0xFFF8FAFC),
                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(12),
                              borderSide: BorderSide(color: Colors.grey.shade300),
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      ElevatedButton(
                        onPressed: () {
                          if (_whisperController.text.trim().isNotEmpty) {
                            _sendWhisper(_whisperController.text.trim());
                          }
                        },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.indigoAccent,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                        ),
                        child: const Icon(Icons.send, color: Colors.white, size: 16),
                      ),
                    ],
                  ),

                  const SizedBox(height: 14),

                  // Takeover Button
                  ElevatedButton.icon(
                    onPressed: _takeoverCall,
                    icon: const Icon(Icons.contact_phone, color: Colors.white, size: 18),
                    label: const Text("Take Over Live Call"),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.green,
                      foregroundColor: Colors.white,
                      minimumSize: const Size.fromHeight(44),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDialogBubble(String text, bool isAI) {
    final bg = isAI ? const Color(0xFFEFF6FF) : const Color(0xFFF1F5F9);
    final border = isAI ? Colors.blue.withOpacity(0.3) : Colors.grey.shade300;
    final align = isAI ? CrossAxisAlignment.start : CrossAxisAlignment.end;

    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Column(
        crossAxisAlignment: align,
        children: [
          Text(
            isAI ? "🤖 AI Assistant" : "👤 Customer",
            style: TextStyle(color: Colors.grey.shade600, fontSize: 10, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 4),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: bg,
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: border),
            ),
            child: Text(
              text,
              style: const TextStyle(color: Color(0xFF0F172A), fontSize: 13),
            ),
          ),
        ],
      ),
    );
  }
}
