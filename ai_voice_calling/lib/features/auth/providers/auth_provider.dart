import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/network/websocket_provider.dart';
import '../../../core/storage/token_storage.dart';
import '../../calls/services/call_event_listener.dart';
import '../models/login_request.dart';
import '../repositories/auth_repository.dart';

final authProvider =
    StateNotifierProvider<AuthNotifier, AuthState>(
  (ref) {
    return AuthNotifier(ref);
  },
);

class AuthNotifier extends StateNotifier<AuthState> {
  AuthNotifier(this.ref)
      : super(
          const AuthState(),
        );

  final Ref ref;

  final AuthRepository _repository =
      AuthRepository.instance;

  Future<bool> login({
    required String email,
    required String password,
  }) async {
    try {
      state = state.copyWith(
        isLoading: true,
        error: null,
      );

      final response = await _repository.login(
        LoginRequest(
          email: email,
          password: password,
        ),
      );

      await TokenStorage.instance.saveToken(
        response.accessToken,
      );

      state = state.copyWith(
        isLoading: false,
        isAuthenticated: true,
      );

      return true;
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );

      return false;
    }
  }

  Future<void> logout() async {
    // Stop listening for WebSocket events
    CallEventListener.instance.stop();

    // Disconnect WebSocket
    await ref
        .read(websocketProvider.notifier)
        .disconnect();

    // Remove saved token
    await TokenStorage.instance.clearToken();

    // Reset authentication state
    state = const AuthState();
  }
}

class AuthState {
  final bool isLoading;

  final bool isAuthenticated;

  final String? error;

  const AuthState({
    this.isLoading = false,
    this.isAuthenticated = false,
    this.error,
  });

  AuthState copyWith({
    bool? isLoading,
    bool? isAuthenticated,
    String? error,
  }) {
    return AuthState(
      isLoading:
          isLoading ?? this.isLoading,
      isAuthenticated:
          isAuthenticated ??
              this.isAuthenticated,
      error: error,
    );
  }
}