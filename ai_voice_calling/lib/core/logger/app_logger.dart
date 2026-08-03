import 'dart:async';
import 'package:logger/logger.dart';

class AppLogger {
  AppLogger._();

  static final StreamController<String> _logStreamController =
      StreamController<String>.broadcast();

  static Stream<String> get logStream => _logStreamController.stream;

  static final Logger logger = Logger(
    filter: ProductionFilter(),
    output: MemoryAndConsoleOutput(_logStreamController),
    printer: PrettyPrinter(
      methodCount: 0,
      errorMethodCount: 5,
      lineLength: 100,
      colors: true,
      printEmojis: true,
      printTime: false,
    ),
  );
}

class MemoryAndConsoleOutput extends LogOutput {
  final StreamController<String> streamController;
  final ConsoleOutput _consoleOutput = ConsoleOutput();

  MemoryAndConsoleOutput(this.streamController);

  @override
  Future<void> init() async {
    await _consoleOutput.init();
  }

  @override
  void output(OutputEvent event) {
    _consoleOutput.output(event);
    for (var line in event.lines) {
      streamController.add(line);
    }
  }

  @override
  Future<void> destroy() async {
    await _consoleOutput.destroy();
  }
}