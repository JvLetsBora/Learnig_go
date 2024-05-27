import 'package:flutter/material.dart';
import 'package:flutter_application_1/components/image_uploder.dart';
import 'package:flutter_application_1/components/task_list.dart';
import 'package:flutter_application_1/controllers/task.dart';
import 'package:flutter_application_1/models/task.dart';



class SegundaTela extends StatefulWidget {
  const SegundaTela({super.key, required this.idUser});

  final int idUser;
  

  @override
  State<SegundaTela> createState() => _SegundaTelaState();
}

class _SegundaTelaState extends State<SegundaTela> {
  late Future<User> futureUser;
  int _selectedIndex = 0;
  final TasksController _controller = TasksController();
  final TextEditingController _controllerTitle = TextEditingController();
  final TextEditingController _controllerDescription = TextEditingController();

  void _reloand(){
        setState(() {
      futureUser = _controller.fetchUser(widget.idUser); // Recarrega os dados do usuário após criar uma nova tarefa
    });
    _controllerTitle.text = "";
    _controllerDescription.text = "";
    
  }

    void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

    void _deleteTaskAndRefreshList(int id) {
      _controller.deleteTaskt(id);
      _reloand();
    }

    void _updateTaskAndRefreshList(int id) {
      _controller.updateTask( id,_controllerTitle.text, _controllerDescription.text);
      _reloand();
    }
    Future<void> _createTaskAndRefreshList() async {
    await _controller.createTask( widget.idUser,_controllerTitle.text, _controllerDescription.text);
    _reloand();
  }
  

  @override
  void initState() {
    super.initState();
    futureUser = _controller.fetchUser(widget.idUser);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _selectedIndex == 0
          ? AppBar(title: const Text("Editor de tasks")) : AppBar(title: const Text("Editor de Imagens")) ,
      body: _selectedIndex == 0 ? FutureBuilder<User>(
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
                      return TaskTile(
                            task: task,
                            onDelete: () => _deleteTaskAndRefreshList(task.id),
                            onUpdate: () => _updateTaskAndRefreshList(task.id),
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
      ) : const ImageUploader(),
    bottomNavigationBar: BottomNavigationBar(
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.task),
            label: 'Tasks',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.image),
            label: 'Imagens',
          ),
        ],
        currentIndex: _selectedIndex,
        selectedItemColor: Colors.blue,
        onTap: _onItemTapped,
      ),
    );
  }
}

