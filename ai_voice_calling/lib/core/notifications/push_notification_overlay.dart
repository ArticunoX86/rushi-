import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Since the websocket provider isn't directly exposed in a way we can easily listen globally
// without refactoring the whole app, we'll expose a static event bus for the overlay.
class NotificationEventBus {
  static final StreamController<Map<String, dynamic>> _controller = StreamController.broadcast();
  static Stream<Map<String, dynamic>> get onNotification => _controller.stream;
  static void fire(Map<String, dynamic> payload) => _controller.add(payload);
}

class PushNotificationOverlay extends StatefulWidget {
  final Widget child;

  const PushNotificationOverlay({super.key, required this.child});

  @override
  State<PushNotificationOverlay> createState() => _PushNotificationOverlayState();
}

class _PushNotificationOverlayState extends State<PushNotificationOverlay> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<Offset> _offsetAnimation;
  String _title = "";
  String _message = "";
  bool _isVisible = false;
  StreamSubscription? _sub;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: const Duration(milliseconds: 500));
    _offsetAnimation = Tween<Offset>(begin: const Offset(0.0, -1.5), end: const Offset(0.0, 0.0))
        .animate(CurvedAnimation(parent: _controller, curve: Curves.easeOutBack));

    _sub = NotificationEventBus.onNotification.listen((payload) {
      if (mounted) {
        setState(() {
          _title = "🔥 Hot Lead Alert";
          _message = payload['message'] ?? "A high-value lead is ready for followup!";
          _isVisible = true;
        });
        _showNotification();
      }
    });
  }

  void _showNotification() async {
    _controller.forward();
    await Future.delayed(const Duration(seconds: 4));
    if (mounted) {
      await _controller.reverse();
      if (mounted) {
        setState(() {
          _isVisible = false;
        });
      }
    }
  }

  @override
  void dispose() {
    _sub?.cancel();
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        widget.child,
        if (_isVisible)
          Positioned(
            top: 60,
          left: 20,
          right: 20,
          child: SlideTransition(
            position: _offsetAnimation,
            child: Material(
              color: Colors.transparent,
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: const [
                    BoxShadow(color: Colors.black26, blurRadius: 20, offset: Offset(0, 10)),
                  ],
                  border: Border.all(color: Colors.orangeAccent.withOpacity(0.5), width: 1.5),
                ),
                child: Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: Colors.orange.shade50,
                        shape: BoxShape.circle,
                      ),
                      child: const Icon(Icons.local_fire_department, color: Colors.orangeAccent, size: 28),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            _title,
                            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Color(0xFF0F172A),),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            _message,
                            style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }
}
