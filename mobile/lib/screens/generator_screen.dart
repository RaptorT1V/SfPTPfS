import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'middle_screen.dart';

class GeneratorScreen extends StatefulWidget {
  @override
  _GeneratorScreenState createState() => _GeneratorScreenState();
}

class _GeneratorScreenState extends State<GeneratorScreen> {
  bool isGeneratorRunning = false;

  Future<void> startGenerator() async {
    try {
      final response = await http.post(Uri.parse('http://127.0.0.1:8000/generator/start'));
      if (response.statusCode == 200) {
        setState(() {
          isGeneratorRunning = true;
        });
        _showPopup("Генератор успешно запущен. Погнали!");
      }
    } catch (e) {
      _showPopup("Э-э-э, не газуй на поворотах!\napp.py не запущен. Зайди в PyCharm и запусти его, если хочешь, чтобы генератор заработал!");
    }
  }

  Future<void> stopGenerator() async {
    try {
      final response = await http.post(Uri.parse('http://127.0.0.1:8000/generator/stop'));
      if (response.statusCode == 200) {
        setState(() {
          isGeneratorRunning = false;
        });
      _showPopup("Генератор остановлен. Спокойной ночи!");
      }
    } catch (e) {
      _showPopup("Стопандэпало! Кого ты останавливать собрался?\napp.py не запущен. То есть сервак ваще отсутствует в этой реальности!");
    }
  }

  void _showPopup(String message) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          content: Text(message),
          actions: <Widget>[
            Center(
              child: TextButton(
                child: Text("Зашибись"),
                onPressed: () => Navigator.of(context).pop(),
              ),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Панель управления генератором")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              isGeneratorRunning ? "Генератор работает" : "Генератор отдыхает",
              style: TextStyle(
                fontSize: 18,
                color: isGeneratorRunning ? Colors.green : Colors.red,
                fontWeight: FontWeight.bold,
                decoration: TextDecoration.underline,
                fontFamily: 'Times New Roman'
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: isGeneratorRunning ? stopGenerator : startGenerator,
              child: Text(isGeneratorRunning ? "Остановить генератор" : "Запустить генератор"),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => MiddleScreen()),
        ),
        child: Icon(Icons.arrow_forward),
      ),
    );
  }
}
