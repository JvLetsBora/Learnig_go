import 'dart:convert';

import 'package:flutter/material.dart';
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

Future<Task> createTask(String title, String description) async {
  final response = await http.post(
    Uri.parse('http://10.150.8.240:8000/users/1/tasks/'),
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
  final response = await http.put(
    Uri.parse('http://10.150.8.240:8000/tasks/$taskId'),
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
  final response = await http.delete(
    Uri.parse('http://10.150.8.240:8000/tasks/$taskId'),
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
  final response = await http.get(Uri.parse('http://10.150.8.240:8000/users/1/'));

  if (response.statusCode == 200) {
    return User.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to load user');
  }
}

class SegundaTela extends StatefulWidget {
  const SegundaTela({super.key, required this.idUser});

  final String idUser;
  

  @override
  State<SegundaTela> createState() => _SegundaTelaState();
}

class _SegundaTelaState extends State<SegundaTela> {
  late Future<User> futureUser;

  final TextEditingController _controllerTitle = TextEditingController();
  final TextEditingController _controllerDescription = TextEditingController();
  


  Future<void> _createTaskAndRefreshList() async {
    await createTask(_controllerTitle.text, _controllerDescription.text);
    setState(() {
      futureUser = fetchUser(1); // Recarrega os dados do usuário após criar uma nova tarefa
    });
    _controllerTitle.text = "";
    _controllerDescription.text = "";
  }

    Future<void> _updateTaskAndRefreshList(int id) async {
    await updateTask(id, _controllerTitle.text , _controllerDescription.text);
    setState(() {
      futureUser = fetchUser(1); // Recarrega os dados do usuário após criar uma nova tarefa
    });
    _controllerTitle.text = "";
    _controllerDescription.text = "";
  }



  Future<void> _deleteTaskAndRefreshList(int id) async {
    await deleteTask(id);
    setState(() {
      futureUser = fetchUser(1); // Recarrega os dados do usuário após criar uma nova tarefa
    });
  }

  @override
  void initState() {
    super.initState();
    futureUser = fetchUser(1);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Oi Mundo")),
      body: FutureBuilder<User>(
        future: futureUser,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Text('Error: ${snapshot.error}');
          } else if (snapshot.hasData) {
            return Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Text('Email: ${snapshot.data!.email}'),
                const SizedBox(height: 20),
                const Text('Tasks:'),
                Expanded(
                  child: ListView.builder(
                    itemCount: snapshot.data!.tasks.length,
                    itemBuilder: (context, index) {
                      final task = snapshot.data!.tasks[index];
                      return 
                      ListTile(
                            style: ListTileStyle.list,
                            title: Text(task.title, style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 20, overflow: TextOverflow.fade)),
                            subtitle: Text(task.description),
                            trailing: Row( mainAxisSize: MainAxisSize.min,
                              children: [
                                Padding( padding: const EdgeInsets.all(8.0), 
                                  child: ElevatedButton(
                                    onPressed: () {
                                      _deleteTaskAndRefreshList(task.id);
                        
                                    },
                                  child: const Icon(Icons.delete),
                              ) ),
                                  Padding(
                                    padding: const EdgeInsets.all(8.0),
                                    child: ElevatedButton(
                                      onPressed: () {
                                        _updateTaskAndRefreshList(task.id);
                                                            
                                      },
                                    child: const Icon(Icons.edit),
                                                                  ),
                                  )
                              ],
                            ),
                            
                          );
                    },
                  ),
                ),
                const SizedBox(height: 20),
                const Text('Create Task:'),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: TextField(
                    controller: _controllerTitle,
                    decoration: const InputDecoration(hintText: 'Enter Title'),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: TextField(
                    controller: _controllerDescription,
                    decoration: const InputDecoration(hintText: 'Enter Description'),
                  ),
                ),
                ElevatedButton(
                  onPressed: () {
                    setState(() {
                      _createTaskAndRefreshList();
                    });
                    
                  },
                  child: const Text('Create Task'),
                ),
              ],
            );
          } else {
            return const Text('No data found');
          }
        },
      ),
    );
  }
}

