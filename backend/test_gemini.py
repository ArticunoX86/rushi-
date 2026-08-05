import google.generativeai as genai
import os

genai.configure(api_key="AQ.Ab8RN6KhG78uOu6NN6anr0Xpyq5tkvTnJjq5wnQtkSvC5uZxjQ")
model = genai.GenerativeModel('gemini-2.0-flash')
try:
    response = model.generate_content("Hello")
    print("Success:", response.text)
except Exception as e:
    print("Error:", str(e))
