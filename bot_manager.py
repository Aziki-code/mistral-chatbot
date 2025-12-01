#!/usr/bin/env python3
"""
Bot Manager
Central orchestrator for all AI chatbots
Initializes and manages multiple bot instances
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

from base_bot import BaseBot
from mistral_bot import MistralBot
from github_copilot_bot import GitHubCopilotBot


class BotManager:
    """Manages multiple AI chatbot instances"""
    
    def __init__(self):
        """Initialize bot manager"""
        self.bots: Dict[str, BaseBot] = {}
        self.default_bot_id: Optional[str] = None
        
    def initialize_all(self) -> None:
        """
        Initialize all available bots
        Attempts to initialize Mistral AI and GitHub Copilot
        """
        print("=" * 60)
        print("Initializing AI Chatbots...")
        print("=" * 60)
        
        # Load environment variables
        load_dotenv()
        
        # Initialize Mistral AI bot
        mistral = MistralBot()
        if mistral.is_available:
            self.bots["mistral"] = mistral
            if not self.default_bot_id:
                self.default_bot_id = "mistral"
        
        # Initialize GitHub Copilot bot
        github = GitHubCopilotBot()
        if github.is_available:
            self.bots["github-copilot"] = github
            if not self.default_bot_id:
                self.default_bot_id = "github-copilot"
        
        # Summary
        print("=" * 60)
        if self.bots:
            print(f"✓ {len(self.bots)} bot(s) initialized")
            print(f"  Available: {', '.join([b.get_display_name() for b in self.bots.values()])}")
            print(f"  Default: {self.get_bot(self.default_bot_id).get_display_name()}")
        else:
            print("⚠️  No bots available! Check your .env configuration:")
            print("   - MISTRAL_API_KEY for Mistral AI")
            print("   - GITHUB_TOKEN for GitHub Copilot")
            raise RuntimeError("No AI bots available")
        print("=" * 60)
    
    def get_bot(self, bot_id: str) -> Optional[BaseBot]:
        """
        Get bot instance by ID
        
        Args:
            bot_id: Bot identifier ("mistral" or "github-copilot")
            
        Returns:
            BaseBot: Bot instance or None if not found
        """
        return self.bots.get(bot_id)
    
    def get_default_bot(self) -> BaseBot:
        """
        Get default bot instance
        
        Returns:
            BaseBot: Default bot (prioritizes Mistral AI)
        """
        if self.default_bot_id:
            return self.bots[self.default_bot_id]
        raise RuntimeError("No default bot available")
    
    def is_bot_available(self, bot_id: str) -> bool:
        """
        Check if specific bot is available
        
        Args:
            bot_id: Bot identifier
            
        Returns:
            bool: True if bot exists and is initialized
        """
        bot = self.get_bot(bot_id)
        return bot is not None and bot.is_available
    
    def get_available_bots(self) -> List[Dict[str, any]]:
        """
        Get list of all available bots with metadata
        
        Returns:
            list: List of bot info dicts
        """
        return [bot.get_model_info() for bot in self.bots.values()]
    
    def chat(self, bot_id: str, messages: List[Dict[str, str]], model: str = None) -> str:
        """
        Send chat request to specific bot
        
        Args:
            bot_id: Bot identifier
            messages: Message history
            model: Optional model override
            
        Returns:
            str: Bot response
            
        Raises:
            ValueError: If bot not available
        """
        bot = self.get_bot(bot_id)
        if not bot:
            available = ', '.join(self.bots.keys())
            raise ValueError(f"Bot '{bot_id}' not available. Available: {available}")
        
        return bot.chat_complete(messages, model)


# Global singleton instance
_bot_manager: Optional[BotManager] = None


def get_bot_manager() -> BotManager:
    """
    Get global bot manager instance (singleton)
    
    Returns:
        BotManager: Global bot manager
    """
    global _bot_manager
    if _bot_manager is None:
        _bot_manager = BotManager()
        _bot_manager.initialize_all()
    return _bot_manager


def main():
    """Main function for testing bot manager"""
    try:
        # Initialize manager
        manager = get_bot_manager()
        
        # Show available bots
        print("\n📋 Available Bots:")
        for bot_info in manager.get_available_bots():
            print(f"   {bot_info['icon']} {bot_info['name']} - {bot_info['provider']}")
        
        # Test chat with default bot
        print("\n💬 Testing default bot...")
        default_bot = manager.get_default_bot()
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one sentence."}
        ]
        
        response = default_bot.chat_complete(messages)
        print(f"   {default_bot.get_display_name()}: {response}")
        
        print("\n✓ All systems operational!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
