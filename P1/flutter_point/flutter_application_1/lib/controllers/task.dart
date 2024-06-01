import 'package:flutter_application_1/models/task.dart';


class TasksController {
  final TasksModel _model = TasksModel();

  Future<void> startEnv() async{
     await _model.startEnv();
  }
  
  Future<User> fetchUser(int id) async{
    return _model.fetchUser(id);
  }

  Future<void> updateTask(int id, String controllerTitle, String controllerDescription) async {
    await _model.updateTask(id, controllerTitle , controllerDescription);
  }

  Future<void> createTask(int id ,String controllerTitle, String controllerDescription) async {
    await _model.createTask( id, controllerTitle, controllerDescription );
  }

  Future<void> deleteTaskt(int id) async {
    await _model.deleteTask(id);
  }
}