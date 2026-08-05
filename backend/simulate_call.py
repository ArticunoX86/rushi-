import requests
import uuid
import sys
import time

# Configuration
BASE_URL = "http://127.0.0.1:8000"
CHAT_ENDPOINT = f"{BASE_URL}/ai/chat"

# Generate dummy UUIDs for testing
test_lead_id = str(uuid.uuid4())
test_call_id = str(uuid.uuid4())

def check_backend_status():
    """Ensure the backend is running before trying to chat."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend is connected and healthy.")
            return True
    except requests.exceptions.ConnectionError:
        pass
    
    print("❌ Cannot connect to Backend.")
    print(f"Please make sure the FastAPI server is running on {BASE_URL}")
    return False

def simulate_conversation():
    print("======================================================")
    print("🤖 NexaVoice AI Local Testing Terminal")
    print("======================================================")
    print(f"Session Call ID: {test_call_id}")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    
    # We loop to allow a continuous conversation, building up history
    while True:
        try:
            # 1. Capture customer voice / text
            user_message = input("👨 Customer: ")
            
            if user_message.strip().lower() in ['exit', 'quit']:
                print("\nEnding simulated call.")
                break
                
            if not user_message.strip():
                continue
                
            # 2. Send request to the AI Brain endpoint
            payload = {
                "lead_id": test_lead_id,
                "call_id": test_call_id,
                "message": user_message
            }
            
            # Add a slight delay for realism (latency)
            start_time = time.time()
            response = requests.post(CHAT_ENDPOINT, json=payload)
            end_time = time.time()
            
            # 3. Print the AI's response
            if response.status_code == 200:
                data = response.json()
                ai_reply = data.get("reply", "No reply generated.")
                print(f"🤖 AI Agent: {ai_reply}")
                
                # Print debug data if the AI extracted CRM information
                extracted_data = {k: v for k, v in data.items() if k != "reply" and v is not None}
                if extracted_data:
                    print(f"   [CRM Auto-Extraction]: {extracted_data}")
                    
                print(f"   [Latency: {round((end_time - start_time) * 1000)}ms]\n")
                
            else:
                print(f"⚠️ Error {response.status_code}: {response.text}\n")
                
        except KeyboardInterrupt:
            print("\nEnding simulated call.")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            break

if __name__ == "__main__":
    if check_backend_status():
        print("Starting simulated call loop...\n")
        simulate_conversation()
