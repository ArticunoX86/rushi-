import requests

ENDPOINT = 'http://127.0.0.1:8000/ai/chat'
msgs = [
    'Hello? Who is this?',
    'Oh, wait, are you a real person or a bot? Sounds like a robot.',
    'Ah okay, gotcha. Yeah I was looking at some apartments.',
    'I mostly want a 3 BHK in Mumbai, budget around 1.5 Crores.',
    'Actually, what are the exact legal fees and stamp duty costs?',
    'Alright, sounds good. Sure, send me the details on WhatsApp.'
]
call_id = 'c1234567-89ab-cdef-0123-456789abcdef'
lead_id = 'c1234567-89ab-cdef-0123-456789abcdef'

print("--- STARTING HUMAN-LIKE AI TEST CALL ---")
for m in msgs:
    print(f"\n👨 Customer: {m}")
    res = requests.post(ENDPOINT, json={'lead_id': lead_id, 'call_id': call_id, 'message': m})
    if res.status_code == 200:
        print(f"🤖 AI Agent: {res.json().get('reply')}")
    else:
        print(f"❌ ERROR: {res.status_code} - {res.text}")
print("\n--- CALL COMPLETED ---")
