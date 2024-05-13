import 'dart:convert';
import 'package:http/http.dart' as http;

class Task {
  final String title;
  final String description;
  final int ownerId;

  Task({
    required this.title, 
    required this.description, 
    required this.ownerId
  });

  factory Task.fromMap(Map<String, dynamic> map) {
    return Task(
      title: map['title'], 
      description: map['description'], 
      ownerId: map['owner_id'] // 'owner_id' em vez de 'ownerId' conforme fornecido na resposta JSON
    );
  }
}

class UserModel {
  final String email;
  final bool isActive;
  final List<Task> tasks;

  UserModel({
    required this.email, 
    required this.isActive, 
    required this.tasks
  });

  factory UserModel.fromMap(Map<String, dynamic> map) {
    return UserModel(
      email: map["email"], 
      isActive: map["is_active"], // 'is_active' em vez de 'isActive' conforme fornecido na resposta JSON
      tasks: List<Task>.from((map["tasks"] as List).map((task) => Task.fromMap(task)))
    );
  }
}

