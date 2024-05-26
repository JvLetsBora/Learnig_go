import 'package:flutter/material.dart';
import 'package:flutter_application_1/models/task.dart';

class TaskTile extends StatelessWidget {
  final Task task;
  final VoidCallback onDelete;
  final VoidCallback onUpdate;

  const TaskTile({
    super.key,
    required this.task,
    required this.onDelete,
    required this.onUpdate,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      style: ListTileStyle.list,
      title: Text(
        task.title,
        style: const TextStyle(
          fontWeight: FontWeight.w800,
          fontSize: 20,
          overflow: TextOverflow.fade,
        ),
      ),
      subtitle: Text(task.description),
      trailing: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: ElevatedButton(
              onPressed: onDelete,
              child: const Icon(Icons.delete),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: ElevatedButton(
              onPressed: onUpdate,
              child: const Icon(Icons.edit),
            ),
          ),
        ],
      ),
    );
  }
}
