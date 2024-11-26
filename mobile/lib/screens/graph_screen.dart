import 'package:flutter/material.dart';
import 'middle_screen.dart';

class GraphScreen extends StatefulWidget {
  @override
  _GraphScreenState createState() => _GraphScreenState();
}

class _GraphScreenState extends State<GraphScreen> {
  String selectedUnit = "Unit 1";
  String selectedParameter = "Parameter 1";
  Duration selectedStart = Duration(minutes: 10);
  Duration selectedEnd = Duration(minutes: 0);

  void _updateGraph() async {
    // Тут будет осуществляться запрос к серверу с данными, которые выбрал пользователь (агрегат, параметр, время)
    // И здесь же будет отображаться график
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Настройки графика")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            DropdownButton<String>(
              value: selectedUnit,
              items: ["Unit 1", "Unit 2", "Unit 3", "Unit 4"].map((unit) {
                return DropdownMenuItem(value: unit, child: Text(unit));
              }).toList(),
              onChanged: (value) {
                setState(() {
                  selectedUnit = value!;
                });
              },
            ),
            DropdownButton<String>(
              value: selectedParameter,
              items: ["Parameter 1", "Parameter 2", "Parameter 3"].map((param) {
                return DropdownMenuItem(value: param, child: Text(param));
              }).toList(),
              onChanged: (value) {
                setState(() {
                  selectedParameter = value!;
                });
              },
            ),
            Text("Начало: ${selectedStart.inMinutes} минут назад"),
            Slider(
              min: 0,
              max: 60,
              value: selectedStart.inMinutes.toDouble(),
              onChanged: (value) {
                setState(() {
                  selectedStart = Duration(minutes: value.toInt());
                });
              },
            ),
            Text("Конец: ${selectedEnd.inMinutes} минут назад"),
            Slider(
              min: 0,
              max: selectedStart.inMinutes.toDouble(),
              value: selectedEnd.inMinutes.toDouble(),
              onChanged: (value) {
                setState(() {
                  selectedEnd = Duration(minutes: value.toInt());
                });
              },
            ),
            ElevatedButton(
              onPressed: _updateGraph,
              child: Text("Построить график"),
            ),
          ],
        ),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.startDocked,
      floatingActionButton: FloatingActionButton(
        onPressed: () => Navigator.pop(context),
        child: Icon(Icons.arrow_back),
      ),
    );
  }
}