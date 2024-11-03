import 'package:flutter/material.dart';
import 'middle_screen.dart';

class GraphScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Графики, графики и ещё раз графики")),
      body: Center(child: Text("Graph configuration options will be here.")),
      floatingActionButtonLocation: FloatingActionButtonLocation.startDocked,
      floatingActionButton: FloatingActionButton(
        onPressed: () => Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => MiddleScreen()),
        ),
        child: Icon(Icons.arrow_back),
      ),
    );
  }
}
