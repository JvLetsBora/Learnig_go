import 'dart:convert';

import 'package:flutter_application_1/data/http/http_client.dart';
import 'package:flutter_application_1/data/models/user.dart';

abstract class IUserReposity{
  Future <UserModel> getUsers();
}

class UserReposity implements IUserReposity {
  final IHttpClient client;

  UserReposity({required this.client});


  @override
  Future<UserModel> getUsers() async {
   final response =  await client.get(url: "http://127.0.0.1:8000/users/1/");

   if (response.statusCode == 200){
      UserModel users = UserModel(email: '', isActive: false, tasks: []);

      final body = jsonDecode(response.body);

      // ignore: avoid_print
      print(body);

      body.map((item){
        final UserModel user = UserModel.fromMap(item);
        users = user;
      }).toList();
      return users;
    } else{
      throw Exception;
    }
  

  }


}