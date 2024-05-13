import 'package:flutter/material.dart';

import 'package:http/http.dart' as http;


class SegundaTela extends StatefulWidget {
  const SegundaTela({super.key});

  @override
  State<SegundaTela> createState() => _SegundaTelaState();
}

class _SegundaTelaState extends State<SegundaTela> {
  final TextEditingController _controller = TextEditingController();
  String _saida = 'oiiiiiiiii';
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Minha segunda tela'),
      ),
      body: Column(
        children: <Widget>[
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: TextField(
              controller: _controller,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Digite seu nome',
              ),
            ),
          ),
          ElevatedButton(
            onPressed: () async {
              var resposta = await http.get(Uri.parse('http://10.0.2.2:35288/users/${_controller.text}/'));
              // Para trabalhar com a saída como JSON/Map
              //var respostaProcessada = jsonDecode(resposta.body);

              setState(() {
                _saida = resposta.body;
              });
            },
            child: const Text("Consultar"),
          ),
          Text(_saida),
        ],
      ),
    );
  }
}