class CallJob {
  final String id;

  final String customerName;

  final String phoneNumber;

  final String status;

  final String priority;

  final String scriptName;

  final DateTime createdAt;

  const CallJob({
    required this.id,
    required this.customerName,
    required this.phoneNumber,
    required this.status,
    required this.priority,
    required this.scriptName,
    required this.createdAt,
  });

  factory CallJob.fromJson(
    Map<String, dynamic> json,
  ) {
    return CallJob(
      id: json["id"] as String,

      customerName:
          json["customer_name"] as String,

      phoneNumber:
          json["phone_number"] as String,

      status: json["status"] as String,

      priority: json["priority"] as String,

      scriptName:
          json["script_name"] as String,

      createdAt: DateTime.parse(
        json["created_at"],
      ),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "customer_name": customerName,
      "phone_number": phoneNumber,
      "status": status,
      "priority": priority,
      "script_name": scriptName,
      "created_at": createdAt.toIso8601String(),
    };
  }

  CallJob copyWith({
    String? id,
    String? customerName,
    String? phoneNumber,
    String? status,
    String? priority,
    String? scriptName,
    DateTime? createdAt,
  }) {
    return CallJob(
      id: id ?? this.id,
      customerName:
          customerName ?? this.customerName,
      phoneNumber:
          phoneNumber ?? this.phoneNumber,
      status: status ?? this.status,
      priority: priority ?? this.priority,
      scriptName:
          scriptName ?? this.scriptName,
      createdAt:
          createdAt ?? this.createdAt,
    );
  }
}