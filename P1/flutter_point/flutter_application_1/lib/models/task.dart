import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class Task {
  final String title;
  final String description;
  final int id;
  final int ownerId;

  Task({
    required this.title,
    required this.description,
    required this.id,
    required this.ownerId,
  });

  factory Task.fromJson(Map<String, dynamic> json) {
    return Task(
      title: json['title'] ?? '',
      description: json['description'] ?? '',
      id: json['id'] ?? 0,
      ownerId: json['owner_id'] ?? 0,
    );
  }
}

class User {
  final String email;
  final int id;
  final bool isActive;
  final List<Task> tasks;

  User({
    required this.email,
    required this.id,
    required this.isActive,
    required this.tasks,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    List<Task> tasks = [];
    if (json['tasks'] != null) {
      tasks = List<Task>.from(json['tasks'].map((task) => Task.fromJson(task)));
    }

    return User(
      email: json['email'] ?? '',
      id: json['id'] ?? 0,
      isActive: json['is_active'] ?? false,
      tasks: tasks,
    );
  }
}



class TasksModel{

  String host = dotenv.env['HOST'] ?? '172.29.192.1';

  Future<String> startEnv() async { 
    await dotenv.load(fileName: ".env");
    host = dotenv.env['HOST'] ?? '172.29.192.1';
    return dotenv.env['HOST'] ?? '172.29.192.1';
  }
  
  


Future<Task> createTask( int userId, String title, String description) async {
  host = await startEnv();
  final response = await http.post(
    Uri.parse('http://$host:8001/api/users/$userId/tasks/'),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{
      'title': title,
      'description': description
    }),
  );

  if (response.statusCode == 200) {
    
    return Task.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to create Task.');
  }
}


Future<Task> updateTask(int taskId, String title, String description) async {
  host = await startEnv();
  final response = await http.put(
    Uri.parse('http://$host:8001/api/tasks/$taskId'),
     headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{
      'title': title,
      'description': description
    }),
  );

  if (response.statusCode == 200) {
    
    return Task.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to create Task.');
  }
}

Future<Task> deleteTask(int taskId) async {
  host = await startEnv();
  final response = await http.delete(
    Uri.parse('http://$host:8001/api/tasks/$taskId'),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
  );

  if (response.statusCode == 200) {
    
    return Task.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to create Task.');
  }
}


Future<User> fetchUser(int userId) async {
  host = await startEnv();
  final response = await http.get(Uri.parse('http://$host:8001/api/users/$userId'));

  if (response.statusCode == 200) {
    return User.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to load user');
  }
}
}