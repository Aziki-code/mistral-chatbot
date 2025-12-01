#!/usr/bin/env python3
"""
Simple bot test script
Tests the bot manager and available bots
"""

import os
from dotenv import load_dotenv
from bot_manager import get_bot_manager

# Load .env file
load_dotenv()

def main():
    try:
        # Initialize bot manager
        manager = get_bot_manager()
        
        # Show available bots
        print("\n" + "="*60)
        print("Available AI Bots:")
        print("="*60)
        for bot_info in manager.get_available_bots():
            status = "✓" if bot_info["available"] else "✗"
            print(f"{status} {bot_info['icon']} {bot_info['name']} ({bot_info['provider']})")
        
        # Test default bot
        print("\n" + "="*60)
        print("Testing Default Bot:")
        print("="*60)
        
        default_bot = manager.get_default_bot()
        user_message = "Hello, are you working? Answer in one sentence."
        
        print(f"User: {user_message}")
        print(f"\nBot ({default_bot.get_display_name()}):")
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Be concise."},
            {"role": "user", "content": user_message}
        ]
        
        response = default_bot.chat_complete(messages)
        print(f"{response}")
        
        print("\n" + "="*60)
        print("✓ Bot test successful!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

