import 'package:flutter/material.dart';
import 'package:flutter_application_1/data/models/user.dart';

class TasksPage extends StatelessWidget {
  final List<Task> tasks;

  const TasksPage({super.key, required this.tasks});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tarefas'),
      ),
      body: ListView.builder(
        itemCount: tasks.length,
        itemBuilder: (context, index) {
          final task = tasks[index];
          return ListTile(
            title: Text(task.title),
            subtitle: Text(task.description),
            // Aqui você pode adicionar mais informações da tarefa, se necessário
          );
        },
      ),
    );
  }
}
