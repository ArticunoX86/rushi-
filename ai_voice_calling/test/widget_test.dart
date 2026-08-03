import 'package:flutter_test/flutter_test.dart';
import 'package:ai_voice_calling/app/app.dart';

void main() {
  testWidgets('App loads successfully', (tester) async {
    await tester.pumpWidget(
      const AIVoiceCallingApp(),
    );

    expect(find.text('AI Voice Calling'), findsOneWidget);
  });
}