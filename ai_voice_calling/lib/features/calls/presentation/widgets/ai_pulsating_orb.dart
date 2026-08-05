import 'package:flutter/material.dart';

class AiPulsatingOrb extends StatefulWidget {
  final bool isSpeaking;
  final double size;

  const AiPulsatingOrb({
    super.key,
    required this.isSpeaking,
    this.size = 180.0,
  });

  @override
  State<AiPulsatingOrb> createState() => _AiPulsatingOrbState();
}

class _AiPulsatingOrbState extends State<AiPulsatingOrb>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    );
    _animation = Tween<double>(begin: 0.85, end: 1.15).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );

    if (widget.isSpeaking) {
      _controller.repeat(reverse: true);
    }
  }

  @override
  void didUpdateWidget(AiPulsatingOrb oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.isSpeaking != oldWidget.isSpeaking) {
      if (widget.isSpeaking) {
        _controller.repeat(reverse: true);
      } else {
        _controller.animateTo(0.0,
            duration: const Duration(milliseconds: 800));
      }
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _animation,
      builder: (context, child) {
        return Transform.scale(
          scale: widget.isSpeaking ? _animation.value : 1.0,
          child: Container(
            width: widget.size,
            height: widget.size,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              gradient: RadialGradient(
                colors: [
                  Colors.cyanAccent.withOpacity(0.8),
                  Colors.blue.shade900.withOpacity(0.5),
                  Colors.transparent,
                ],
                stops: const [0.3, 0.7, 1.0],
              ),
              boxShadow: widget.isSpeaking
                  ? [
                      BoxShadow(
                        color: Colors.cyanAccent.withOpacity(0.6),
                        blurRadius: 50 * _animation.value,
                        spreadRadius: 15 * _animation.value,
                      )
                    ]
                  : [],
            ),
            child: const Center(
              child: Icon(
                Icons.graphic_eq,
                color: Colors.white,
                size: 64,
              ),
            ),
          ),
        );
      },
    );
  }
}
