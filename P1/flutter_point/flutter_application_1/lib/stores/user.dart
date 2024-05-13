

import 'package:flutter/material.dart';
import 'package:flutter_application_1/data/models/user.dart';
import 'package:flutter_application_1/data/repositories/user.dart';

class UserStore{
  final IUserReposity reposity;


  final ValueNotifier<bool> isLoading = ValueNotifier<bool>(true);

  final ValueNotifier<UserModel> state = ValueNotifier<UserModel>(UserModel(email: "", isActive: false, tasks: [],));

  final ValueNotifier<String> erro = ValueNotifier<String>("");

  UserStore({required this.reposity});

  Future getUser() async {
    isLoading.value = true;

    try {
      final result = await reposity.getUsers();
      state.value = result;
    } catch (e){

      erro.value = e.toString();
    }
  }
}