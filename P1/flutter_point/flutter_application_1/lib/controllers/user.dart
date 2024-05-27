import 'package:flutter_application_1/models/user.dart';


class UserController {
  final UserModel _model = UserModel();
  
  Future<void> updateUser(int id, String email, String password) async {
    await _model.updateUser(id, email , password);
  }

  Future<int> createUser(String email, String password) async {
    return await _model.createUser(email, password );
  }

  Future<void> deleteUser(int id) async {
    await _model.deleteUser(id);
  }
}