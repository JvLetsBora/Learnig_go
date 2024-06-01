import 'dart:io';

import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_dotenv/flutter_dotenv.dart';  

class User {
  final String email;
  final String password;

  User({
    required this.email,
    required this.password,

  });

  factory User.fromJson(Map<String, dynamic> json) {

    return User(
      email: json['email'] ?? '',
      password: json['password'] ?? '',
    );
  }
}

Future main() async{
  await dotenv.load(fileName: ".env");


}

class UserModel{
  final String host = dotenv.env['HOST'] ?? '172.29.192.1';
  
  
Future<int> createUser( String email,String password ) async {
  
  final response = await http.post(
    Uri.parse('http://$host:8001/api/users/'),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{
      'email': email,
      'password': password
    }),
  );

  if (response.statusCode == 200) {
      int userId  = jsonDecode(response.body)["id"];
    return userId;
  } else {
    throw Exception('Failed to create User.');
  }
}


Future<User> updateUser(int id, String password, String email) async {
  final response = await http.put(
    Uri.parse('http://$host:8001/api/users/$id'),
     headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{
      'email': email,
      'password': password
      
    }),
  );

  if (response.statusCode == 200) {
    
    return User.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to create Task.');
  }
}

Future<int> deleteUser(int id) async {
  final response = await http.delete(
    Uri.parse('http://$host:8001/api/users/$id'),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
  );

  if (response.statusCode == 200) {
    
    return HttpStatus.ok;
  } else {
    throw Exception('Failed to create Task.');
  }
}
}