import 'package:flutter/material.dart';

class AppCard extends StatelessWidget {
  final Widget child;

  final EdgeInsetsGeometry? padding;

  const AppCard({
    super.key,
    required this.child,
    this.padding,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,

      shadowColor: Colors.black12,

      color: Colors.white,

      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
      ),

      child: Padding(
        padding: padding ??
            const EdgeInsets.all(
              20,
            ),
        child: child,
      ),
    );
  }
}