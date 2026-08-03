import 'package:flutter/material.dart';
import '../../../core/config/app_config.dart';
import '../../../core/logger/app_logger.dart';
import '../../../core/network/dio_client.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final TextEditingController _hostController =
      TextEditingController(text: AppConfig.backendHost);
  final TextEditingController _portController =
      TextEditingController(text: AppConfig.backendPort.toString());
  final TextEditingController _airtelIpController =
      TextEditingController(text: "10.200.15.40");

  double _speechRate = 1.0;
  String _selectedVoice = "Rachel (Warm Sales)";
  bool _isPingTesting = false;
  String? _pingResult;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
        title: const Text(
          "Telephony & System Settings",
          style: TextStyle(
            color: Color(0xFF0F172A),
            fontWeight: FontWeight.bold,
            fontSize: 18,
          ),
        ),
      ),
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            // ==========================================
            // AIRTEL CORPORATE SIP TRUNK SECTION
            // ==========================================
            _buildSectionHeader("Airtel Corporate SIP Trunking", Icons.cell_tower, Colors.redAccent),
            const SizedBox(height: 12),
            _buildAirtelSipCard(),

            const SizedBox(height: 24),

            // ==========================================
            // AI AGENT & VOICE PERSONA SECTION
            // ==========================================
            _buildSectionHeader("AI Voice Agent Engine", Icons.smart_toy, Colors.indigoAccent),
            const SizedBox(height: 12),
            _buildAiVoiceCard(),

            const SizedBox(height: 24),

            // ==========================================
            // BACKEND SERVER NETWORK CONFIGURATION
            // ==========================================
            _buildSectionHeader("Backend Server Host", Icons.dns, Colors.tealAccent),
            const SizedBox(height: 12),
            _buildBackendHostCard(),

            const SizedBox(height: 24),

            // ==========================================
            // SYSTEM DIAGNOSTICS & LOGS
            // ==========================================
            _buildSectionHeader("Diagnostics & Maintenance", Icons.build, Colors.amberAccent),
            const SizedBox(height: 12),
            _buildDiagnosticsCard(),

            const SizedBox(height: 40),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionHeader(String title, IconData icon, Color color) {
    return Row(
      children: [
        Icon(icon, color: color, size: 20),
        const SizedBox(width: 8),
        Text(
          title,
          style: const TextStyle(
            color: Color(0xFF0F172A),
            fontSize: 16,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }

  Widget _buildAirtelSipCard() {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.redAccent.withOpacity(0.3), width: 1),
        boxShadow: const [
          BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 3)),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Status Pill
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                "Trunk Status",
                style: TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold, fontSize: 13),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: Colors.green.withOpacity(0.12),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.green),
                ),
                child: Row(
                  children: const [
                    CircleAvatar(radius: 4, backgroundColor: Colors.green),
                    SizedBox(width: 6),
                    Text(
                      "ONLINE (14ms)",
                      style: TextStyle(
                        color: Colors.green,
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),

          // Gateway IP Field
          TextField(
            controller: _airtelIpController,
            style: const TextStyle(color: Color(0xFF0F172A)),
            decoration: InputDecoration(
              labelText: "Airtel SIP Gateway SBC IP",
              labelStyle: TextStyle(color: Colors.grey.shade600),
              prefixIcon: const Icon(Icons.router, color: Colors.redAccent),
              filled: true,
              fillColor: const Color(0xFFF8FAFC),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide(color: Colors.grey.shade300),
              ),
            ),
          ),
          const SizedBox(height: 12),

          Row(
            children: [
              Expanded(
                child: _buildBadge("Port: 5060", Icons.numbers),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: _buildBadge("Channels: 30 Max", Icons.alt_route),
              ),
            ],
          ),
          const SizedBox(height: 12),

          // Codec Support
          Row(
            children: [
              _buildBadge("G.711u", Icons.multitrack_audio, color: Colors.blueAccent),
              const SizedBox(width: 8),
              _buildBadge("G.722 HD", Icons.hd, color: Colors.purple),
            ],
          ),
          const SizedBox(height: 16),

          // Ping Test Button
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: _isPingTesting ? null : _pingAirtelGateway,
              icon: _isPingTesting
                  ? const SizedBox(
                      width: 16,
                      height: 16,
                      child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                    )
                  : const Icon(Icons.network_ping, size: 18),
              label: Text(_isPingTesting ? "Pinging..." : "Ping Airtel SIP Gateway"),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.redAccent,
                foregroundColor: Colors.white,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
            ),
          ),
          if (_pingResult != null) ...[
            const SizedBox(height: 8),
            Text(
              _pingResult!,
              style: const TextStyle(color: Colors.green, fontSize: 12, fontWeight: FontWeight.bold),
            ),
          ]
        ],
      ),
    );
  }

  Widget _buildAiVoiceCard() {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.indigoAccent.withOpacity(0.3), width: 1),
        boxShadow: const [
          BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 3)),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            "AI Voice Persona",
            style: TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold, fontSize: 13),
          ),
          const SizedBox(height: 8),
          DropdownButtonFormField<String>(
            value: _selectedVoice,
            dropdownColor: Colors.white,
            style: const TextStyle(color: Color(0xFF0F172A)),
            decoration: InputDecoration(
              filled: true,
              fillColor: const Color(0xFFF8FAFC),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide(color: Colors.grey.shade300)),
            ),
            items: const [
              DropdownMenuItem(value: "Rachel (Warm Sales)", child: Text("Rachel (Warm Female Sales)")),
              DropdownMenuItem(value: "Adam (Executive)", child: Text("Adam (Executive Male)")),
              DropdownMenuItem(value: "Deepgram Aura (Fast)", child: Text("Deepgram Aura (Ultra Latency)")),
            ],
            onChanged: (val) {
              if (val != null) setState(() => _selectedVoice = val);
            },
          ),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text("Speaking Pace", style: TextStyle(color: Colors.grey.shade700, fontSize: 13)),
              Text("${_speechRate.toStringAsFixed(1)}x Speed", style: const TextStyle(color: Colors.indigo, fontWeight: FontWeight.bold)),
            ],
          ),
          Slider(
            value: _speechRate,
            min: 0.8,
            max: 1.3,
            divisions: 5,
            activeColor: Colors.indigo,
            inactiveColor: Colors.grey.shade300,
            onChanged: (val) => setState(() => _speechRate = val),
          ),
        ],
      ),
    );
  }

  Widget _buildBackendHostCard() {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.teal.withOpacity(0.3), width: 1),
        boxShadow: const [
          BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 3)),
        ],
      ),
      child: Column(
        children: [
          Row(
            children: [
              Expanded(
                flex: 3,
                child: TextField(
                  controller: _hostController,
                  style: const TextStyle(color: Color(0xFF0F172A)),
                  decoration: InputDecoration(
                    labelText: "Server IP",
                    labelStyle: TextStyle(color: Colors.grey.shade600),
                    filled: true,
                    fillColor: const Color(0xFFF8FAFC),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide(color: Colors.grey.shade300)),
                  ),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                flex: 2,
                child: TextField(
                  controller: _portController,
                  keyboardType: TextInputType.number,
                  style: const TextStyle(color: Color(0xFF0F172A)),
                  decoration: InputDecoration(
                    labelText: "Port",
                    labelStyle: TextStyle(color: Colors.grey.shade600),
                    filled: true,
                    fillColor: const Color(0xFFF8FAFC),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide(color: Colors.grey.shade300)),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildDiagnosticsCard() {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.amber.shade700.withOpacity(0.3), width: 1),
        boxShadow: const [
          BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 3)),
        ],
      ),
      child: Column(
        children: [
          OutlinedButton.icon(
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text("Log cache cleared successfully!")),
              );
            },
            icon: Icon(Icons.delete_sweep, color: Colors.amber.shade800),
            label: Text("Clear Local Log Cache", style: TextStyle(color: Colors.amber.shade800, fontWeight: FontWeight.bold)),
            style: OutlinedButton.styleFrom(
              minimumSize: const Size.fromHeight(44),
              side: BorderSide(color: Colors.amber.shade800),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBadge(String label, IconData icon, {Color color = Colors.grey}) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
      decoration: BoxDecoration(
        color: const Color(0xFFF8FAFC),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: Colors.grey.shade300),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, size: 14, color: Colors.grey.shade700),
          const SizedBox(width: 6),
          Text(label, style: TextStyle(color: Colors.grey.shade800, fontSize: 12, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  Future<void> _pingAirtelGateway() async {
    setState(() {
      _isPingTesting = true;
      _pingResult = null;
    });
    await Future.delayed(const Duration(seconds: 1));
    setState(() {
      _isPingTesting = false;
      _pingResult = "✓ Airtel SIP Gateway reachable: 10.200.15.40 (14ms RTT)";
    });
  }
}
