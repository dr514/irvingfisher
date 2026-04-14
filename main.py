# main.py
# Powershell CLI Client for JimmySims

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("JIMMY_API_TOKEN")
SERVER_URL = "http://127.0.0.1:5000/chat"

print("====================================")
print(" JimmySims Agent - Powershell CLI")
print("====================================")
print("Type 'exit' or 'quit' to leave.")
print("Tell Jimmy if you're switching to your phone to get a passcode!\n")

while True:
    try:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            break
        if not user_input.strip():
            continue
            
        headers = {
            "X-API-Token": API_TOKEN or "",
            "Content-Type": "application/json"
        }
        
        response = requests.post(SERVER_URL, json={"message": user_input}, headers=headers)
        
        if response.status_code == 200:
            print(f"\nJimmy: {response.json().get('response')}\n")
        else:
            print(f"\n[Error] Server returned {response.status_code}: {response.text}\n")
            
    except requests.exceptions.ConnectionError:
        print("\n[Error] Cannot connect to server. Please run 'python server.py' in another terminal window first.\n")
    except KeyboardInterrupt:
        break

print("Goodbye!")
