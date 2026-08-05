import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/network/dio_client.dart';

class SalesforceSyncScreen extends ConsumerStatefulWidget {
  const SalesforceSyncScreen({super.key});

  @override
  ConsumerState<SalesforceSyncScreen> createState() => _SalesforceSyncScreenState();
}

class _SalesforceSyncScreenState extends ConsumerState<SalesforceSyncScreen> {
  bool _isLoading = true;
  bool _isSyncing = false;
  Map<String, dynamic>? _status;
  List<String> _logs = [];
  int _syncedCount = 0;
  int _skippedCount = 0;

  @override
  void initState() {
    super.initState();
    _fetchStatus();
  }

  Future<void> _fetchStatus() async {
    try {
      final response = await DioClient.instance.dio.get('/salesforce/status');
      if (response.statusCode == 200 && response.data != null) {
        setState(() {
          _status = response.data;
          _isLoading = false;
        });
      }
    } catch (e) {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _triggerSync() async {
    setState(() {
      _isSyncing = true;
      _logs = ["Initiating Salesforce OAuth handshake...", "Requesting leads from Salesforce Sandbox Lead object..."];
      _syncedCount = 0;
      _skippedCount = 0;
    });

    try {
      final response = await DioClient.instance.dio.post('/salesforce/sync');
      if (response.statusCode == 200 && response.data != null) {
        final data = response.data;
        setState(() {
          _isSyncing = false;
          _syncedCount = data['synced_count'] ?? 0;
          _skippedCount = data['skipped_count'] ?? 0;
          _logs = List<String>.from(data['logs'] ?? []);
        });
        
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: Color(0xFF7C3AED),
            content: Text("Salesforce Sync Completed! Synced: $_syncedCount, Skipped: $_skippedCount"),
          ),
        );
      }
    } catch (e) {
      setState(() {
        _isSyncing = false;
        _logs.add("Sync error: Connection lost or credentials invalid.");
      });
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Salesforce synchronization failed")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
        title: const Text(
          "Salesforce Integration",
          style: TextStyle(
            color: Color(0xFF0F172A),
            fontWeight: FontWeight.bold,
            fontSize: 18,
          ),
        ),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator(color: Color(0xFF7C3AED)))
          : SafeArea(
              child: ListView(
                padding: const EdgeInsets.all(20),
                children: [
                  _buildConnectionStatusCard(),
                  const SizedBox(height: 20),
                  _buildSyncControlCard(),
                  const SizedBox(height: 20),
                  _buildLogsConsoleCard(),
                ],
              ),
            ),
    );
  }

  Widget _buildConnectionStatusCard() {
    final mode = _status?['integration_mode'] ?? 'Salesforce REST API (Production)';
    final isConfigured = _status?['credentials_configured'] ?? false;

    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: const [
          BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 3)),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: const [
                  Icon(Icons.cloud, color: Color(0xFF7C3AED), size: 24),
                  SizedBox(width: 8),
                  Text(
                    "CRM Credentials",
                    style: TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold, fontSize: 15),
                  ),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: isConfigured ? Colors.green.withOpacity(0.12) : Color(0xFF7C3AED).withOpacity(0.12),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Text(
                  isConfigured ? "CONNECTED" : "DEV SANDBOX",
                  style: TextStyle(
                    color: isConfigured ? Colors.green : Color(0xFF7C3AED),
                    fontSize: 11,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
          const Divider(height: 24),
          _buildStatusRow("Integration Mode", mode),
          const SizedBox(height: 10),
          _buildStatusRow("Sync Object", "Salesforce Lead Table"),
          const SizedBox(height: 10),
          _buildStatusRow("Instance URL", _status?['instance_url'] ?? "https://login.salesforce.com"),
          const SizedBox(height: 10),
          _buildStatusRow("API Version", _status?['api_version'] ?? "v60.0"),
        ],
      ),
    );
  }

  Widget _buildSyncControlCard() {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: const [
          BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 3)),
        ],
      ),
      child: Column(
        children: [
          const Text(
            "Pull Leads from Salesforce CRM",
            style: TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold, fontSize: 14),
          ),
          const SizedBox(height: 6),
          Text(
            "Synchronizes Salesforce prospects into the local PostgreSQL database table to prepare them for AI sales campaigns.",
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.grey.shade500, fontSize: 12),
          ),
          const SizedBox(height: 16),
          if (_isSyncing) ...[
            const LinearProgressIndicator(color: Color(0xFF7C3AED), backgroundColor: Color(0xFFF1F5F9)),
            const SizedBox(height: 12),
          ],
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildMetric("Synced", "$_syncedCount", Colors.green),
              _buildMetric("Skipped", "$_skippedCount", Colors.amber.shade800),
            ],
          ),
          const SizedBox(height: 16),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: _isSyncing ? null : _triggerSync,
              icon: _isSyncing
                  ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                  : const Icon(Icons.sync_alt),
              label: Text(_isSyncing ? "Synchronizing..." : "Trigger Salesforce Sync"),
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFF7C3AED),
                foregroundColor: Colors.white,
                minimumSize: const Size.fromHeight(44),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLogsConsoleCard() {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: const [
          BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 3)),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            "Synchronizer Activity Logs",
            style: TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold, fontSize: 13),
          ),
          const SizedBox(height: 10),
          Container(
            width: double.infinity,
            height: 180,
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: const Color(0xFFF8FAFC),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.grey.shade300),
            ),
            child: _logs.isEmpty
                ? Center(
                    child: Text(
                      "No sync logs compiled. Click 'Trigger Salesforce Sync'.",
                      style: TextStyle(color: Colors.grey.shade500, fontSize: 11),
                    ),
                  )
                : ListView.builder(
                    itemCount: _logs.length,
                    itemBuilder: (context, index) {
                      return Padding(
                        padding: const EdgeInsets.only(bottom: 6),
                        child: Text(
                          _logs[index],
                          style: const TextStyle(
                            color: Color(0xFF0F172A),
                            fontFamily: 'monospace',
                            fontSize: 11,
                          ),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatusRow(String label, String value) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(label, style: TextStyle(color: Colors.grey.shade600, fontSize: 12)),
        Text(value, style: const TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold, fontSize: 12)),
      ],
    );
  }

  Widget _buildMetric(String label, String count, Color color) {
    return Column(
      children: [
        Text(count, style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 20)),
        const SizedBox(height: 2),
        Text(label, style: TextStyle(color: Colors.grey.shade600, fontSize: 11)),
      ],
    );
  }
}
