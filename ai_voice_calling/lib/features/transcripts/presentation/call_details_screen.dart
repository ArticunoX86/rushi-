import 'package:flutter/material.dart';
import 'dart:async';

class CallDetailsScreen extends StatefulWidget {
  final String leadName;
  final double score;

  const CallDetailsScreen({
    super.key,
    required this.leadName,
    required this.score,
  });

  @override
  State<CallDetailsScreen> createState() => _CallDetailsScreenState();
}

class _CallDetailsScreenState extends State<CallDetailsScreen> with SingleTickerProviderStateMixin {
  bool _isPlaying = false;
  double _playbackProgress = 0.0;
  Timer? _playbackTimer;
  late AnimationController _pulseController;

  final List<Map<String, dynamic>> _transcript = [
    {"speaker": "AI", "text": "Hello, this is Rachel from NexaVoice Real Estate. Am I speaking with ${"Lead"}?", "time": "00:02"},
    {"speaker": "Lead", "text": "Yes, speaking. What's this about?", "time": "00:05"},
    {"speaker": "AI", "text": "Great! I'm calling because you recently showed interest in our new 3 BHK luxury villas on our website. I wanted to see if you had any questions.", "time": "00:12"},
    {"speaker": "Lead", "text": "Oh right, yeah. I was just browsing. Are there any corner plots available?", "time": "00:20"},
    {"speaker": "AI", "text": "Yes, we do have a few corner plots left! They offer great natural lighting and extra garden space. Would you be interested in scheduling a quick site visit this weekend?", "time": "00:31"},
    {"speaker": "Lead", "text": "Sure, Saturday morning works for me.", "time": "00:38"},
    {"speaker": "AI", "text": "Perfect! I have you booked for Saturday at 10 AM. You will receive a WhatsApp confirmation shortly. Have a wonderful day!", "time": "00:45"},
  ];

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 1),
    );
  }

  @override
  void dispose() {
    _playbackTimer?.cancel();
    _pulseController.dispose();
    super.dispose();
  }

  void _togglePlayback() {
    setState(() {
      _isPlaying = !_isPlaying;
    });

    if (_isPlaying) {
      _pulseController.repeat(reverse: true);
      _playbackTimer = Timer.periodic(const Duration(milliseconds: 100), (timer) {
        setState(() {
          _playbackProgress += 0.002;
          if (_playbackProgress >= 1.0) {
            _isPlaying = false;
            _playbackProgress = 0.0;
            _pulseController.stop();
            timer.cancel();
          }
        });
      });
    } else {
      _pulseController.stop();
      _playbackTimer?.cancel();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Hero(
      tag: 'recent_call_${widget.leadName}',
      child: Scaffold(
        backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        iconTheme: IconThemeData(color: const Color(0xFF0F172A),),
        title: Text(
          widget.leadName,
          style: TextStyle(color: const Color(0xFF0F172A), fontWeight: FontWeight.bold),
        ),
        actions: [
          Container(
            margin: const EdgeInsets.only(right: 16, top: 12, bottom: 12),
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
            decoration: BoxDecoration(
              color: widget.score >= 80 ? Colors.green.withOpacity(0.1) : Colors.orange.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Center(
              child: Text(
                "Score: ${widget.score.toInt()}",
                style: TextStyle(
                  color: widget.score >= 80 ? Colors.green : Colors.orange,
                  fontWeight: FontWeight.bold,
                  fontSize: 12,
                ),
              ),
            ),
          )
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            _buildAudioPlayer(),
            Expanded(
              child: _buildTranscriptList(),
            ),
          ],
        ),
      ),
      ),
    );
  }

  Widget _buildAudioPlayer() {
    return Container(
      margin: const EdgeInsets.all(20),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: const Color(0xFF0F172A),
        borderRadius: BorderRadius.circular(24),
        boxShadow: const [
          BoxShadow(color: Colors.black12, blurRadius: 15, offset: Offset(0, 5)),
        ],
        border: Border.all(color: Theme.of(context).brightness == Brightness.dark ? const Color(0xFF3F3F5A) : Colors.grey.shade200),
      ),
      child: Column(
        children: [
          Row(
            children: [
              const Icon(Icons.graphic_eq, color: Colors.blueAccent),
              const SizedBox(width: 8),
              const Text("AI Call Recording", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              const Spacer(),
              AnimatedBuilder(
                animation: _pulseController,
                builder: (context, child) {
                  return Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: _isPlaying ? Colors.redAccent.withOpacity(_pulseController.value * 0.2 + 0.1) : Colors.grey.shade200,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      _isPlaying ? "PLAYING" : "PAUSED",
                      style: TextStyle(
                        color: _isPlaying ? Colors.redAccent : Colors.grey.shade400,
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  );
                },
              ),
            ],
          ),
          const SizedBox(height: 20),
          Row(
            children: [
              GestureDetector(
                onTap: _togglePlayback,
                child: Container(
                  height: 48,
                  width: 48,
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(colors: [Colors.blueAccent, Colors.indigo]),
                    shape: BoxShape.circle,
                    boxShadow: [
                      BoxShadow(color: Colors.blueAccent.withOpacity(0.4), blurRadius: 8, offset: const Offset(0, 4)),
                    ],
                  ),
                  child: Icon(_isPlaying ? Icons.pause : Icons.play_arrow, color: const Color(0xFF0F172A)),
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  children: [
                    SliderTheme(
                      data: SliderThemeData(
                        trackHeight: 4,
                        thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 6),
                        overlayShape: const RoundSliderOverlayShape(overlayRadius: 14),
                        activeTrackColor: Colors.blueAccent,
                        inactiveTrackColor: Colors.grey.shade200,
                        thumbColor: Colors.blueAccent,
                      ),
                      child: Slider(
                        value: _playbackProgress,
                        onChanged: (val) {
                          setState(() {
                            _playbackProgress = val;
                          });
                        },
                      ),
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text("00:${(_playbackProgress * 45).toInt().toString().padLeft(2, '0')}", style: const TextStyle(fontSize: 12, color: Colors.grey)),
                        const Text("00:45", style: TextStyle(fontSize: 12, color: Colors.grey)),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildTranscriptList() {
    return ListView.builder(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
      itemCount: _transcript.length,
      itemBuilder: (context, index) {
        final msg = _transcript[index];
        final isAI = msg['speaker'] == 'AI';
        
        return Container(
          margin: const EdgeInsets.only(bottom: 20),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              if (isAI) ...[
                const CircleAvatar(
                  backgroundColor: Colors.indigo,
                  radius: 18,
                  child: Icon(Icons.smart_toy, color: const Color(0xFF0F172A), size: 18),
                ),
                const SizedBox(width: 12),
              ],
              Expanded(
                child: Column(
                  crossAxisAlignment: isAI ? CrossAxisAlignment.start : CrossAxisAlignment.end,
                  children: [
                    Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          msg['speaker'],
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 12,
                            color: isAI ? Colors.indigo : Colors.grey.shade400,
                          ),
                        ),
                        const SizedBox(width: 8),
                        Text(
                          msg['time'],
                          style: const TextStyle(fontSize: 10, color: Colors.grey),
                        ),
                      ],
                    ),
                    const SizedBox(height: 6),
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: isAI ? Colors.white : Colors.indigoAccent,
                        borderRadius: BorderRadius.only(
                          topLeft: const Radius.circular(16),
                          topRight: const Radius.circular(16),
                          bottomLeft: isAI ? const Radius.circular(4) : const Radius.circular(16),
                          bottomRight: isAI ? const Radius.circular(16) : const Radius.circular(4),
                        ),
                        boxShadow: const [
                          BoxShadow(color: Colors.black12, blurRadius: 4, offset: Offset(0, 2)),
                        ],
                      ),
                      child: Text(
                        msg['text'].replaceAll('Lead', widget.leadName),
                        style: TextStyle(
                          color: isAI ? Colors.white : Colors.white,
                          height: 1.4,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              if (!isAI) ...[
                const SizedBox(width: 12),
                const CircleAvatar(
                  backgroundColor: Colors.grey,
                  radius: 18,
                  child: Icon(Icons.person, color: const Color(0xFF0F172A), size: 18),
                ),
              ],
            ],
          ),
        );
      },
    );
  }
}
