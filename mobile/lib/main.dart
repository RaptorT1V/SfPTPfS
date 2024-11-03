import 'package:flutter/material.dart';
import 'screens/generator_screen.dart';
import 'screens/middle_screen.dart';
import 'screens/graph_screen.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SfPTPfS App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: MiddleScreen(),
      routes: {
        '/generator': (context) => GeneratorScreen(),
        '/middle': (context) => MiddleScreen(),
        '/graph': (context) => GraphScreen(),
      },
    );
  }
}
