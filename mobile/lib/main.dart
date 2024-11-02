import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: GeneratorScreen(),
    );
  }
}

class GeneratorScreen extends StatefulWidget {
  @override
  _GeneratorScreenState createState() => _GeneratorScreenState();
}

class _GeneratorScreenState extends State<GeneratorScreen> {
  bool isGeneratorRunning = false;

  @override
  void initState() {
    super.initState();
    checkServerStatus();
  }

  Future<void> startGenerator() async {
    try {
      final response = await http.post(Uri.parse('http://127.0.0.1:8000/generator/start'));
      if (response.statusCode == 200) {
        setState(() {
          isGeneratorRunning = true;
        });
        _showPopup("Generator started successfully");
      }
    } catch (e) {
      _showPopup("Э-э-э, не газуй на поворотах! app.py не запущен. Зайди в PyCharm и запусти его!");
    }
  }

  Future<void> stopGenerator() async {
    try {
      final response = await http.post(Uri.parse('http://127.0.0.1:8000/generator/stop'));
      if (response.statusCode == 200) {
        setState(() {
          isGeneratorRunning = false;
        });
        _showPopup("Generator stopped successfully");
      }
    } catch (e) {
      _showPopup("Куда собрался стопать? app.py не запущен! То есть сервак ваще отсутствует!");
    }
  }

  Future<void> checkServerStatus() async {
    try {
      final response = await http.get(Uri.parse('http://127.0.0.1:8000/'));
      setState(() {
        isGeneratorRunning = response.statusCode == 200;
      });
    } catch (e) {
      setState(() {
        isGeneratorRunning = false;
      });
      _showPopup("Мне кое-кто нашептал, что app.py не запущен. То есть сервак ваще отсутствует. Зайди в PyCharm и запусти его!");
    }
  }

  void _showPopup(String message) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          content: Text(message),
          actions: <Widget>[
            TextButton(
              child: Text("OK"),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Generator Control")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              isGeneratorRunning ? "Generator is running" : "Generator is not running",
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
              child: Text(isGeneratorRunning ? "Stop Generator" : "Start Generator"),
            ),
          ],
        ),
      ),
    );
  }
}
