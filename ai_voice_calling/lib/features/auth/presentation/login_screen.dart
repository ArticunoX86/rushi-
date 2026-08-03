import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:ai_voice_calling/core/config/app_config.dart';
import 'package:ai_voice_calling/core/network/websocket_provider.dart';
import 'package:ai_voice_calling/features/auth/providers/auth_provider.dart';
import 'package:ai_voice_calling/features/navigation/navigation_screen.dart';

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen>
    with SingleTickerProviderStateMixin {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  bool _obscurePassword = true;
  late AnimationController _animController;
  late Animation<double> _fadeAnim;
  late Animation<Offset> _slideAnim;

  // NexaVoice brand colors
  static const Color _emerald = Color(0xFF1B8B4B);
  static const Color _emeraldLight = Color(0xFF26A35A);
  static const Color _charcoal = Color(0xFF1C1C2E);
  static const Color _surface = Color(0xFFF4F7F5);

  @override
  void initState() {
    super.initState();
    _animController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 900),
    );
    _fadeAnim = CurvedAnimation(
      parent: _animController,
      curve: Curves.easeOut,
    );
    _slideAnim = Tween<Offset>(
      begin: const Offset(0, 0.12),
      end: Offset.zero,
    ).animate(CurvedAnimation(
      parent: _animController,
      curve: Curves.easeOutCubic,
    ));
    _animController.forward();
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _animController.dispose();
    super.dispose();
  }

  Future<void> _login() async {
    final success = await ref.read(authProvider.notifier).login(
          email: _emailController.text.trim(),
          password: _passwordController.text,
        );

    if (!mounted) return;

    final authState = ref.read(authProvider);

    if (!success) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          backgroundColor: const Color(0xFF1C1C2E),
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          content: Row(
            children: [
              const Icon(Icons.error_outline, color: Colors.redAccent, size: 20),
              const SizedBox(width: 10),
              Expanded(
                child: Text(
                  authState.error ?? 'Login failed. Please try again.',
                  style: const TextStyle(color: Colors.white),
                ),
              ),
            ],
          ),
        ),
      );
      return;
    }

    try {
      await ref.read(websocketProvider.notifier).connect();
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          backgroundColor: const Color(0xFF1C1C2E),
          content: Row(
            children: [
              const Icon(Icons.error_outline, color: Colors.redAccent, size: 20),
              const SizedBox(width: 10),
              Expanded(
                child: Text(
                  'Connection failed. Backend might be offline.',
                  style: const TextStyle(color: Colors.white),
                ),
              ),
            ],
          ),
        ),
      );
      return;
    }

    if (!mounted) return;

    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(builder: (_) => const NavigationScreen()),
      (route) => false,
    );
  }

  @override
  Widget build(BuildContext context) {
    final auth = ref.watch(authProvider);
    final size = MediaQuery.of(context).size;

    return Scaffold(
      backgroundColor: _surface,
      body: Stack(
        children: [
          // ── Background decoration ──────────────────────────────────
          Positioned(
            top: -80,
            right: -80,
            child: Container(
              width: 260,
              height: 260,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: _emerald.withOpacity(0.08),
              ),
            ),
          ),
          Positioned(
            bottom: -60,
            left: -60,
            child: Container(
              width: 200,
              height: 200,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: _emerald.withOpacity(0.06),
              ),
            ),
          ),

          // ── Main content ──────────────────────────────────────────
          SafeArea(
            child: Center(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 24),
                child: FadeTransition(
                  opacity: _fadeAnim,
                  child: SlideTransition(
                    position: _slideAnim,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        // ── Logo ─────────────────────────────────────
                        Center(
                          child: Image.asset(
                            'assets/images/nexavoice_logo.png',
                            height: size.height * 0.14,
                            fit: BoxFit.contain,
                          ),
                        ),

                        const SizedBox(height: 12),

                        // ── Tagline ──────────────────────────────────
                        const Center(
                          child: Text(
                            'Future of CRM',
                            style: TextStyle(
                              fontSize: 13,
                              letterSpacing: 2.5,
                              fontWeight: FontWeight.w600,
                              color: _emerald,
                            ),
                          ),
                        ),

                        const SizedBox(height: 44),

                        // ── Login Card ───────────────────────────────
                        Container(
                          padding: const EdgeInsets.all(28),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(24),
                            boxShadow: [
                              BoxShadow(
                                color: _charcoal.withOpacity(0.07),
                                blurRadius: 32,
                                offset: const Offset(0, 8),
                              ),
                              BoxShadow(
                                color: _emerald.withOpacity(0.05),
                                blurRadius: 20,
                                offset: const Offset(0, 4),
                              ),
                            ],
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.stretch,
                            children: [
                              // Card header
                              Text(
                                'Welcome back',
                                style: TextStyle(
                                  fontSize: 22,
                                  fontWeight: FontWeight.bold,
                                  color: _charcoal,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                'Sign in to your NexaVoice account',
                                style: TextStyle(
                                  fontSize: 13,
                                  color: Colors.grey.shade500,
                                ),
                              ),

                              const SizedBox(height: 28),

                              // Email field
                              _NexaTextField(
                                controller: _emailController,
                                label: 'Email address',
                                icon: Icons.email_outlined,
                                keyboardType: TextInputType.emailAddress,
                              ),

                              const SizedBox(height: 16),

                              // Password field
                              _NexaTextField(
                                controller: _passwordController,
                                label: 'Password',
                                icon: Icons.lock_outline_rounded,
                                obscureText: _obscurePassword,
                                suffixIcon: IconButton(
                                  icon: Icon(
                                    _obscurePassword
                                        ? Icons.visibility_off_outlined
                                        : Icons.visibility_outlined,
                                    color: Colors.grey.shade400,
                                    size: 20,
                                  ),
                                  onPressed: () => setState(
                                      () => _obscurePassword = !_obscurePassword),
                                ),
                              ),

                              const SizedBox(height: 28),

                              // Sign In button
                              _NexaSignInButton(
                                loading: auth.isLoading,
                                onPressed: _login,
                              ),
                            ],
                          ),
                        ),

                        const SizedBox(height: 36),

                        // ── Footer ───────────────────────────────────
                        Column(
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Container(
                                  width: 6,
                                  height: 6,
                                  decoration: const BoxDecoration(
                                    shape: BoxShape.circle,
                                    color: _emerald,
                                  ),
                                ),
                                const SizedBox(width: 8),
                                Text(
                                  'Powered by Gemini AI · Salesforce CRM',
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: Colors.grey.shade400,
                                    letterSpacing: 0.4,
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 6),
                            Text(
                              'v${AppConfig.appVersion}',
                              textAlign: TextAlign.center,
                              style: TextStyle(
                                fontSize: 11,
                                color: Colors.grey.shade400,
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// ── Reusable NexaVoice Text Field ───────────────────────────────────────────

class _NexaTextField extends StatelessWidget {
  final TextEditingController controller;
  final String label;
  final IconData icon;
  final bool obscureText;
  final TextInputType? keyboardType;
  final Widget? suffixIcon;

  const _NexaTextField({
    required this.controller,
    required this.label,
    required this.icon,
    this.obscureText = false,
    this.keyboardType,
    this.suffixIcon,
  });

  static const Color _emerald = Color(0xFF1B8B4B);
  static const Color _charcoal = Color(0xFF1C1C2E);

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      obscureText: obscureText,
      keyboardType: keyboardType,
      style: const TextStyle(fontSize: 15, color: _charcoal),
      decoration: InputDecoration(
        labelText: label,
        labelStyle: TextStyle(color: Colors.grey.shade500, fontSize: 14),
        prefixIcon: Icon(icon, color: _emerald, size: 20),
        suffixIcon: suffixIcon,
        filled: true,
        fillColor: const Color(0xFFF8FAF9),
        contentPadding:
            const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: BorderSide(color: Colors.grey.shade200),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: BorderSide(color: Colors.grey.shade200),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: const BorderSide(color: _emerald, width: 1.8),
        ),
      ),
    );
  }
}

// ── NexaVoice Sign In Button ─────────────────────────────────────────────────

class _NexaSignInButton extends StatelessWidget {
  final bool loading;
  final VoidCallback onPressed;

  const _NexaSignInButton({
    required this.loading,
    required this.onPressed,
  });

  static const Color _emerald = Color(0xFF1B8B4B);
  static const Color _emeraldLight = Color(0xFF26A35A);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: loading ? null : onPressed,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        height: 54,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(14),
          gradient: LinearGradient(
            colors: loading
                ? [Colors.grey.shade300, Colors.grey.shade300]
                : [_emeraldLight, _emerald],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          boxShadow: loading
              ? []
              : [
                  BoxShadow(
                    color: _emerald.withOpacity(0.35),
                    blurRadius: 16,
                    offset: const Offset(0, 6),
                  ),
                ],
        ),
        child: Center(
          child: loading
              ? const SizedBox(
                  width: 22,
                  height: 22,
                  child: CircularProgressIndicator(
                    strokeWidth: 2.5,
                    valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                  ),
                )
              : const Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      'Sign In',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 16,
                        fontWeight: FontWeight.w700,
                        letterSpacing: 0.5,
                      ),
                    ),
                    SizedBox(width: 8),
                    Icon(Icons.arrow_forward_rounded,
                        color: Colors.white, size: 18),
                  ],
                ),
        ),
      ),
    );
  }
}