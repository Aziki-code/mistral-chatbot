#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from mistralai import Mistral

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in .env")

# Create Mistral client
client = Mistral(api_key=api_key)

# Example message to chatbot
user_message = "Hello, are you working?"

response = client.chat.complete(
    model="mistral-small-latest",
    messages=[{"role": "user", "content": user_message}]
)

# Print bot response
print("Bot responds:", response.choices[0].message.content)

