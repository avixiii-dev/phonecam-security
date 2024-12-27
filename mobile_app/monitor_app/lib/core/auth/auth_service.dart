import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../network/api_client.dart';

class AuthService {
  final ApiClient _apiClient;
  final FlutterSecureStorage _storage;

  AuthService()
      : _apiClient = ApiClient(),
        _storage = const FlutterSecureStorage();

  Future<void> login(String username, String password) async {
    try {
      final response = await _apiClient.post('/auth/login/', data: {
        'username': username,
        'password': password,
      });

      final token = response.data['access'];
      final refreshToken = response.data['refresh'];

      await _storage.write(key: 'access_token', value: token);
      await _storage.write(key: 'refresh_token', value: refreshToken);
    } catch (e) {
      rethrow;
    }
  }

  Future<void> register({
    required String username,
    required String email,
    required String password,
    required String firstName,
    required String lastName,
  }) async {
    try {
      await _apiClient.post('/auth/register/', data: {
        'username': username,
        'email': email,
        'password': password,
        'first_name': firstName,
        'last_name': lastName,
      });
    } catch (e) {
      rethrow;
    }
  }

  Future<void> logout() async {
    await _storage.delete(key: 'access_token');
    await _storage.delete(key: 'refresh_token');
  }

  Future<bool> isAuthenticated() async {
    final token = await _storage.read(key: 'access_token');
    return token != null;
  }

  Future<Map<String, dynamic>> getUserProfile() async {
    try {
      final response = await _apiClient.get('/auth/profile/');
      return response.data;
    } catch (e) {
      rethrow;
    }
  }
}
