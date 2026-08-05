import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_animate/flutter_animate.dart';

import '../../../../services/realtime_audio_service.dart';
import '../../services/call_action_service.dart';
import '../widgets/ai_pulsating_orb.dart';
import '../../models/call_job.dart';

class ActiveCallScreen extends ConsumerStatefulWidget {
  final CallJob job;

  const ActiveCallScreen({
    super.key,
    required this.job,
  });

  @override
  ConsumerState<ActiveCallScreen> createState() => _ActiveCallScreenState();
}

class _ActiveCallScreenState extends ConsumerState<ActiveCallScreen> {
  bool _isMuted = false;
  bool _isCallActive = true;

  @override
  void initState() {
    super.initState();
    // In a real app, this would start the WebRTC connection or native streaming
    RealTimeAudioService.instance.registerCallId(widget.job.id);
    RealTimeAudioService.instance.startStreaming(widget.job.id);
    CallActionService.instance.acceptCall(callId: widget.job.id);
  }

  void _endCall() async {
    setState(() {
      _isCallActive = false;
    });
    
    await RealTimeAudioService.instance.stopStreaming();
    CallActionService.instance.rejectCall(callId: widget.job.id);
    
    if (mounted) {
      context.pop();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC), // Light premium mode
      body: SafeArea(
        child: Column(
          children: [
            const SizedBox(height: 40),
            
            // Header Info
            Column(
              children: [
                Text(
                  "ACTIVE CALL",
                  style: TextStyle(
                    color: const Color(0xFF7C3AED).withOpacity(0.8),
                    fontSize: 14,
                    letterSpacing: 2,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  widget.job.customerName,
                  style: const TextStyle(
                    color: const Color(0xFF0F172A),
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  widget.job.phoneNumber,
                  style: TextStyle(
                    color: Colors.grey.shade600,
                    fontSize: 18,
                  ),
                ),
              ],
            ).animate().fade(duration: 600.ms).slideY(begin: -0.2, end: 0, curve: Curves.easeOutCubic),
            
            const Spacer(),
            
            // AI Visualizer
            AiPulsatingOrb(
              isSpeaking: _isCallActive,
              size: 200,
            ).animate().fade(delay: 300.ms, duration: 800.ms),
            
            const Spacer(),
            
            // Call Controls
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 40),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: const BorderRadius.vertical(top: Radius.circular(40)),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  // Mute Button
                  GestureDetector(
                    onTap: () {
                      setState(() {
                        _isMuted = !_isMuted;
                      });
                    },
                    child: Container(
                      width: 65,
                      height: 65,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: _isMuted ? const Color(0xFF0F172A) : Colors.grey.shade200,
                      ),
                      child: Icon(
                        _isMuted ? Icons.mic_off : Icons.mic,
                        color: _isMuted ? Colors.white : const Color(0xFF0F172A),
                        size: 28,
                      ),
                    ),
                  ),
                  
                  // End Call Button
                  GestureDetector(
                    onTap: _endCall,
                    child: Container(
                      width: 75,
                      height: 75,
                      decoration: const BoxDecoration(
                        shape: BoxShape.circle,
                        color: Colors.redAccent,
                      ),
                      child: const Icon(
                        Icons.call_end,
                        color: Colors.white,
                        size: 36,
                      ),
                    ),
                  ),
                  
                  // Speaker Button
                  GestureDetector(
                    onTap: () {},
                    child: Container(
                      width: 65,
                      height: 65,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: const Color(0xFF0F172A).withOpacity(0.1),
                      ),
                      child: const Icon(
                        Icons.volume_up,
                        color: const Color(0xFF0F172A),
                        size: 28,
                      ),
                    ),
                  ),
                ],
              ),
            ).animate().fade(delay: 500.ms, duration: 500.ms).slideY(begin: 0.5, end: 0, curve: Curves.easeOutCubic),
          ],
        ),
      ),
    );
  }
}
