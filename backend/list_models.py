import google.generativeai as genai
import os

genai.configure(api_key="AQ.Ab8RN6L2Oek6Pp7GNcG4aY5Q864wt7C4Q9My3ZrDdMMBFU19vA")
print("Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
