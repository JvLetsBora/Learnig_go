import 'package:flutter/material.dart';
import 'package:flutter_application_1/models/task.dart';

class UserStore{
  final TasksModel reposity;


  final ValueNotifier<bool> isLoading = ValueNotifier<bool>(true);

  final ValueNotifier<User> state = ValueNotifier<User>(User(id: 1, email: "", isActive: false, tasks: [],));

  final ValueNotifier<String> erro = ValueNotifier<String>("");

  UserStore({required this.reposity});

  Future getUser( int id ) async {
    isLoading.value = false;

    try {
      final result = await reposity.fetchUser(id);
      state.value = result;
    } catch (e){

      erro.value = e.toString();
    }
  }
}
