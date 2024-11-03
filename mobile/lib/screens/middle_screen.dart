import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'generator_screen.dart';
import 'graph_screen.dart';

class MiddleScreen extends StatefulWidget {
  @override
  _MiddleScreenState createState() => _MiddleScreenState();
}

class _MiddleScreenState extends State<MiddleScreen> with SingleTickerProviderStateMixin {
  bool isServerRunning = false;
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    checkServerStatus();
    _controller = AnimationController(vsync: this, duration: Duration(seconds: 3))..repeat(reverse: true);
    _animation = Tween<double>(begin: 0, end: 1).animate(_controller);
  }

  Future<void> checkServerStatus() async {
    try {
      final response = await http.get(Uri.parse('http://127.0.0.1:8000/'));
      setState(() {
        isServerRunning = response.statusCode == 200;
      });
    } catch (e) {
      setState(() {
        isServerRunning = false;
      });
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Состояние сервера + Навигация")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            AnimatedBuilder(
              animation: _animation,
              builder: (context, child) {
                return Container(
                  padding: EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      width: 4,
                      color: Colors.transparent,
                    ),
                    gradient: LinearGradient(
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                      colors: isServerRunning
                          ? [Colors.teal.shade400, Colors.green.shade400]
                          : [Colors.orange.shade700, Colors.red.shade700],
                      stops: [
                        (_animation.value - 0.3).clamp(0.0, 1.0),
                        (_animation.value + 0.3).clamp(0.0, 1.0),
                      ],
                      tileMode: TileMode.mirror,
                    ),
                  ),
                  child: Text(
                    isServerRunning ? "Сервер запущен" : "Сервер не запущен",
                    style: TextStyle(
                      fontSize: 28,
                      color: Colors.white,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                );
              },
            ),
          ],
        ),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
      floatingActionButton: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          FloatingActionButton(
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => GeneratorScreen()),
            ),
            child: Icon(Icons.arrow_back),
          ),
          FloatingActionButton(
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => GraphScreen()),
            ),
            child: Icon(Icons.arrow_forward),
          ),
        ],
      ),
    );
  }
}
