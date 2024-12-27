import 'package:flutter/material.dart';

class AppLogo extends StatelessWidget {
  final double size;
  final Color? color;

  const AppLogo({
    super.key,
    this.size = 100,
    this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        color: color ?? Theme.of(context).primaryColor,
        shape: BoxShape.circle,
      ),
      child: Center(
        child: Icon(
          Icons.monitor,
          size: size * 0.5,
          color: Colors.white,
        ),
      ),
    );
  }
}
