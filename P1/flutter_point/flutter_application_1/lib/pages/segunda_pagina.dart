import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_application_1/data/http/http_client.dart';
import 'package:flutter_application_1/data/repositories/user.dart';
import 'package:flutter_application_1/stores/user.dart';
import 'package:http/http.dart' as http;

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

Future<User> fetchUser(int userId) async {
  final response = await http.get(Uri.parse('http://172.28.16.1:8000/users/$userId/'));

  if (response.statusCode == 200) {
    return User.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to load user');
  }
}

class SegundaTela extends StatefulWidget {
  const SegundaTela({super.key});

  @override
  State<SegundaTela> createState() => _SegundaTelaState();
}

class _SegundaTelaState extends State<SegundaTela> {
  late Future<User> futureUser;

  @override
  void initState() {
    super.initState();
    futureUser = fetchUser(1); // Replace '1' with the actual user id you want to fetch
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Oi Mundo")),
      body: Center(
        child: FutureBuilder<User>(
          future: futureUser,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const CircularProgressIndicator();
            } else if (snapshot.hasError) {
              return Text('Error: ${snapshot.error}');
            } else if (snapshot.hasData) {
              return Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text('Email: ${snapshot.data!.email}'),
                  const SizedBox(height: 20),
                  const Text('Tasks:'),
                  Column(
                    children: snapshot.data!.tasks.map((task) {
                      return ListTile(
                        title: Text(task.title),
                        subtitle: Text(task.description),
                      );
                    }).toList(),
                  ),
                ],
              );
            } else {
              return const Text('No data found');
            }
          },
        ),
      ),
    );
  }
}
