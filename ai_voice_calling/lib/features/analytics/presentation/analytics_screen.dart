import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../../core/network/dio_client.dart';
import '../../transcripts/presentation/call_details_screen.dart';

class AnalyticsScreen extends StatefulWidget {
  const AnalyticsScreen({super.key});

  @override
  State<AnalyticsScreen> createState() => _AnalyticsScreenState();
}

class _AnalyticsScreenState extends State<AnalyticsScreen> {
  bool _isLoading = true;
  Map<String, dynamic>? _data;
  Timer? _autoRefreshTimer;

  @override
  void initState() {
    super.initState();
    _fetchAnalytics(showLoading: true);
    // Real-time live analytics updates every 2 seconds
    _autoRefreshTimer = Timer.periodic(const Duration(seconds: 2), (_) {
      if (mounted) _fetchAnalytics(showLoading: false);
    });
  }

  @override
  void dispose() {
    _autoRefreshTimer?.cancel();
    super.dispose();
  }

  Future<void> _fetchAnalytics({bool showLoading = false}) async {
    if (showLoading) {
      setState(() => _isLoading = true);
      
      // Load cached data first for instant UI response (Offline Caching)
      final prefs = await SharedPreferences.getInstance();
      final cached = prefs.getString('analytics_cache');
      if (cached != null) {
        if (mounted) {
          setState(() {
            _data = jsonDecode(cached);
            _isLoading = false;
          });
        }
      }
    }
    
    try {
      final res = await DioClient.instance.dio.get('/analytics/overview');
      if (res.statusCode == 200 && res.data != null) {
        
        // Save to cache
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('analytics_cache', jsonEncode(res.data['data']));

        if (mounted) {
          setState(() {
            _data = res.data['data'];
            _isLoading = false;
          });
        }
      }
    } catch (e) {
      if (mounted && _data == null) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final kpis = _data?['kpis'] ?? {};
    final outcomes = _data?['outcomes_breakdown'] ?? {};
    final sentiment = _data?['sentiment_analysis'] ?? {};

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
        title: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              "Call Analytics",
              style: TextStyle(
                color: Color(0xFF0F172A),
                fontWeight: FontWeight.bold,
                fontSize: 18,
              ),
            ),
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
              decoration: BoxDecoration(
                color: Colors.green.withOpacity(0.12),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: Colors.green, width: 1),
              ),
              child: Row(
                children: const [
                  CircleAvatar(radius: 3.5, backgroundColor: Colors.green),
                  SizedBox(width: 4),
                  Text(
                    "LIVE",
                    style: TextStyle(
                      color: Colors.green,
                      fontSize: 10,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh, color: Colors.blueAccent),
            onPressed: () => _fetchAnalytics(showLoading: true),
          ),
        ],
      ),
      body: _isLoading && _data == null
          ? const _AnalyticsSkeletonLoader()
          : SafeArea(
              child: ListView(
                padding: const EdgeInsets.all(20),
                children: [
                  // ==========================================
                  // KPI HIGHLIGHT CARDS
                  // ==========================================
                  Row(
                    children: [
                      Expanded(
                        child: _buildKpiCard(
                          "Total Calls",
                          "${kpis['total_calls'] ?? 42}",
                          Icons.phone_forwarded,
                          Colors.blueAccent,
                        ),
                      ),
                      const SizedBox(width: 14),
                      Expanded(
                        child: _buildKpiCard(
                          "Conversion",
                          "${kpis['conversion_rate_pct'] ?? 42.8}%",
                          Icons.insights,
                          Colors.greenAccent,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 14),
                  Row(
                    children: [
                      Expanded(
                        child: _buildKpiCard(
                          "Avg Duration",
                          kpis['avg_call_duration'] ?? "02:45",
                          Icons.timer,
                          Colors.orangeAccent,
                        ),
                      ),
                      const SizedBox(width: 14),
                      Expanded(
                        child: _buildKpiCard(
                          "AI Latency",
                          "${kpis['avg_ai_latency_ms'] ?? 142} ms",
                          Icons.bolt,
                          Colors.purpleAccent,
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: 24),

                  // ==========================================
                  // AIRTEL SIP CHANNEL CONCURRENCY GAUGE
                  // ==========================================
                  _buildSectionTitle("Airtel SIP Trunk Channel Concurrency", Icons.cell_tower),
                  const SizedBox(height: 10),
                  _buildSipChannelGauge(),

                  const SizedBox(height: 24),

                  // ==========================================
                  // AVERAGE LEAD SCORE GAUGE
                  // ==========================================
                  _buildSectionTitle("AI Lead Quality Score", Icons.star_border_purple500),
                  const SizedBox(height: 10),
                  _buildLeadScoreGauge(kpis),

                  const SizedBox(height: 24),

                  // ==========================================
                  // CALL OUTCOME BREAKDOWN
                  // ==========================================
                  _buildSectionTitle("Call Outcome Distribution", Icons.pie_chart),
                  const SizedBox(height: 10),
                  _buildOutcomeBreakdown(outcomes),

                  const SizedBox(height: 24),

                  // ==========================================
                  // PROPERTY PREFERENCE HOTSPOTS
                  // ==========================================
                  _buildSectionTitle("Property Interest Hotspots", Icons.holiday_village),
                  const SizedBox(height: 10),
                  _buildPropertyInterestCard(),

                  const SizedBox(height: 24),

                  // ==========================================
                  // CUSTOMER SENTIMENT METER
                  // ==========================================
                  _buildSectionTitle("Customer Sentiment Analysis", Icons.emoji_emotions),
                  const SizedBox(height: 10),
                  _buildSentimentMeter(sentiment),

                  const SizedBox(height: 24),

                  // ==========================================
                  // RECENT CALL INSIGHTS (TRANSCRIPTS)
                  // ==========================================
                  _buildSectionTitle("Recent Call Insights", Icons.record_voice_over),
                  const SizedBox(height: 10),
                  _buildRecentCallsInsights(),

                  const SizedBox(height: 40),
                ],
              ),
            ),
    );
  }

  Widget _buildSectionTitle(String title, IconData icon) {
    return Row(
      children: [
        Icon(icon, color: Colors.blueAccent, size: 18),
        const SizedBox(width: 8),
        Text(
          title,
          style: TextStyle(
            color: Color(0xFF0F172A),
            fontSize: 16,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }

  Widget _buildKpiCard(String title, String value, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        boxShadow: const [
          BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 3)),
        ],
        border: Border.all(color: color.withOpacity(0.3), width: 1),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 22),
          const SizedBox(height: 12),
          Text(
            value,
            style: TextStyle(
              color: Color(0xFF0F172A),
              fontSize: 22,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            title,
            style: TextStyle(color: Colors.grey.shade600, fontSize: 12),
          ),
        ],
      ),
    );
  }

  Widget _buildSipChannelGauge() {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        boxShadow: const [
          BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 3)),
        ],
        border: Border.all(color: Colors.redAccent.withOpacity(0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: const [
              Text("Active Channels: 4 / 30", style: TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold)),
              Text("13% Utilization", style: TextStyle(color: Colors.green, fontSize: 12, fontWeight: FontWeight.bold)),
            ],
          ),
          const SizedBox(height: 12),
          ClipRRect(
            borderRadius: BorderRadius.circular(10),
            child: const LinearProgressIndicator(
              value: 4 / 30,
              minHeight: 10,
              backgroundColor: Color(0xFFE2E8F0),
              color: Colors.redAccent,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildOutcomeBreakdown(Map<String, dynamic> outcomes) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        boxShadow: const [
          BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 3)),
        ],
      ),
      child: Column(
        children: [
          _buildOutcomeRow("Site Visit Booked", "${outcomes['site_visit_booked'] ?? 8}", 0.42, Colors.green),
          const SizedBox(height: 12),
          _buildOutcomeRow("Interested Lead", "${outcomes['interested'] ?? 18}", 0.35, Colors.blueAccent),
          const SizedBox(height: 12),
          _buildOutcomeRow("Callback Requested", "${outcomes['callback_requested'] ?? 10}", 0.18, Colors.amber.shade800),
          const SizedBox(height: 12),
          _buildOutcomeRow("Not Interested", "${outcomes['not_interested'] ?? 6}", 0.05, Colors.redAccent),
        ],
      ),
    );
  }

  Widget _buildOutcomeRow(String title, String count, double percent, Color color) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(title, style: TextStyle(color: Color(0xFF0F172A), fontSize: 13, fontWeight: FontWeight.w500)),
            Text("$count calls", style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 12)),
          ],
        ),
        const SizedBox(height: 6),
        ClipRRect(
          borderRadius: BorderRadius.circular(6),
          child: LinearProgressIndicator(
            value: percent,
            minHeight: 8,
            backgroundColor: const Color(0xFFE2E8F0),
            color: color,
          ),
        ),
      ],
    );
  }

  Widget _buildPropertyInterestCard() {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        boxShadow: const [
          BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 3)),
        ],
      ),
      child: Column(
        children: [
          _buildPropertyItem("2 BHK Apartment", "45% Interest", Colors.cyan.shade700),
          const SizedBox(height: 10),
          _buildPropertyItem("3 BHK Luxury Villa", "30% Interest", Colors.purple),
          const SizedBox(height: 10),
          _buildPropertyItem("Commercial Shop / Plot", "15% Interest", Colors.orange.shade800),
        ],
      ),
    );
  }

  static Widget _buildPropertyItem(String name, String value, Color color) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Row(
          children: [
            CircleAvatar(radius: 4, backgroundColor: color),
            const SizedBox(width: 8),
            Text(name, style: TextStyle(color: Color(0xFF0F172A), fontSize: 13, fontWeight: FontWeight.w500)),
          ],
        ),
        Text(value, style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 12)),
      ],
    );
  }

  Widget _buildSentimentMeter(Map<String, dynamic> sentiment) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        boxShadow: const [
          BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 3)),
        ],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _buildSentimentItem("Positive", "${sentiment['positive_pct'] ?? 74}%", Colors.green, Icons.sentiment_very_satisfied),
          _buildSentimentItem("Neutral", "${sentiment['neutral_pct'] ?? 18}%", Colors.amber.shade800, Icons.sentiment_neutral),
          _buildSentimentItem("Negative", "${sentiment['negative_pct'] ?? 8}%", Colors.redAccent, Icons.sentiment_dissatisfied),
        ],
      ),
    );
  }

  Widget _buildSentimentItem(String label, String pct, Color color, IconData icon) {
    return Column(
      children: [
        Icon(icon, color: color, size: 28),
        const SizedBox(height: 6),
        Text(pct, style: TextStyle(color: color, fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 2),
        Text(label, style: TextStyle(color: Colors.grey.shade600, fontSize: 11)),
      ],
    );
  }

  // ===============================================
  // NEW LEAD SCORE GAUGE
  // ===============================================
  Widget _buildLeadScoreGauge(Map<String, dynamic> kpis) {
    final double score = (kpis['avg_lead_score'] as num?)?.toDouble() ?? 78.5;
    
    Color scoreColor;
    if (score >= 80) {
      scoreColor = Colors.greenAccent.shade700;
    } else if (score >= 50) {
      scoreColor = Colors.orangeAccent;
    } else {
      scoreColor = Colors.redAccent;
    }

    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        boxShadow: const [
          BoxShadow(color: Colors.black12, blurRadius: 8, offset: Offset(0, 3)),
        ],
        border: Border.all(color: scoreColor.withOpacity(0.3), width: 1),
      ),
      child: Column(
        children: [
          Stack(
            alignment: Alignment.center,
            children: [
              SizedBox(
                height: 100,
                width: 100,
                child: CircularProgressIndicator(
                  value: score / 100,
                  strokeWidth: 10,
                  backgroundColor: const Color(0xFFE2E8F0),
                  color: scoreColor,
                  strokeCap: StrokeCap.round,
                ),
              ),
              Column(
                children: [
                  Text(
                    score.toStringAsFixed(1),
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: scoreColor,
                    ),
                  ),
                  const Text(
                    "/ 100",
                    style: TextStyle(fontSize: 10, color: Colors.grey),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 16),
          const Text(
            "Overall AI Conversion Potential",
            style: TextStyle(
              color: Color(0xFF0F172A),
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }

  // ===============================================
  // NEW RECENT CALL INSIGHTS (TRANSCRIPTS)
  // ===============================================
  Widget _buildRecentCallsInsights() {
    // Mocking recent calls that have a transcript summary and a lead score
    final recentCalls = [
      {"name": "John Doe", "score": 92.0, "summary": "Highly interested in 3 BHK. Requested callback tomorrow.", "sentiment": "Positive"},
      {"name": "Sarah Smith", "score": 45.0, "summary": "Not looking to buy currently. Found the pricing too high.", "sentiment": "Negative"},
      {"name": "Michael Lee", "score": 75.0, "summary": "Asked for a brochure for the commercial plots. Warm lead.", "sentiment": "Neutral"},
    ];

    return SizedBox(
      height: 180,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: recentCalls.length,
        itemBuilder: (context, index) {
          final call = recentCalls[index];
          final score = call['score'] as double;
          
          Color scoreColor = score >= 80 ? Colors.green : (score >= 50 ? Colors.orange : Colors.red);
          
          return Hero(
            tag: 'recent_call_${call['name']}',
            child: Material(
              color: Colors.transparent,
              child: Container(
            width: 280,
            margin: const EdgeInsets.only(right: 16, bottom: 8, top: 4),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              boxShadow: const [
                BoxShadow(color: Colors.black12, blurRadius: 4, offset: Offset(0, 2)),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      call['name'] as String,
                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: scoreColor.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        "Score: ${score.toInt()}",
                        style: TextStyle(color: scoreColor, fontWeight: FontWeight.bold, fontSize: 12),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                Expanded(
                  child: Text(
                    call['summary'] as String,
                    style: TextStyle(color: Colors.grey.shade600, fontSize: 13, height: 1.4),
                    overflow: TextOverflow.fade,
                  ),
                ),
                const SizedBox(height: 8),
                Align(
                  alignment: Alignment.centerRight,
                  child: TextButton.icon(
                    onPressed: () {
                      Navigator.push(
                        context,
                        PageRouteBuilder(
                          transitionDuration: const Duration(milliseconds: 600),
                          reverseTransitionDuration: const Duration(milliseconds: 400),
                          pageBuilder: (context, animation, secondaryAnimation) => FadeTransition(
                            opacity: animation,
                            child: CallDetailsScreen(
                              leadName: call['name'] as String,
                              score: score,
                            ),
                          ),
                        ),
                      );
                    },
                    icon: const Icon(Icons.receipt_long, size: 16),
                    label: const Text("View Transcript", style: TextStyle(fontSize: 12)),
                    style: TextButton.styleFrom(
                      padding: EdgeInsets.zero,
                      minimumSize: const Size(0, 0),
                      tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                    ),
                  ),
                ),
              ],
            ),
            ),
            ),
          );
        },
      ),
    );
  }
}

class _AnalyticsSkeletonLoader extends StatefulWidget {
  const _AnalyticsSkeletonLoader({Key? key}) : super(key: key);

  @override
  State<_AnalyticsSkeletonLoader> createState() => _AnalyticsSkeletonLoaderState();
}

class _AnalyticsSkeletonLoaderState extends State<_AnalyticsSkeletonLoader>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: Tween<double>(begin: 0.4, end: 1.0).animate(_controller),
      child: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            Row(
              children: [
                Expanded(child: _buildSkeletonBox(100)),
                const SizedBox(width: 14),
                Expanded(child: _buildSkeletonBox(100)),
              ],
            ),
            const SizedBox(height: 14),
            Row(
              children: [
                Expanded(child: _buildSkeletonBox(100)),
                const SizedBox(width: 14),
                Expanded(child: _buildSkeletonBox(100)),
              ],
            ),
            const SizedBox(height: 24),
            _buildSkeletonBox(140),
            const SizedBox(height: 24),
            _buildSkeletonBox(160),
            const SizedBox(height: 24),
            _buildSkeletonBox(200),
          ],
        ),
      ),
    );
  }

  Widget _buildSkeletonBox(double height) {
    return Container(
      height: height,
      decoration: BoxDecoration(
        color: Colors.grey.shade200,
        borderRadius: BorderRadius.circular(18),
      ),
    );
  }
}
