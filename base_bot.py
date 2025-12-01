#!/usr/bin/env python3
"""
Base Bot Interface
Abstract class defining common interface for all AI bots
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseBot(ABC):
    """Abstract base class for AI chatbots"""
    
    def __init__(self, name: str):
        """
        Initialize bot
        
        Args:
            name: Display name of the bot
        """
        self.name = name
        self._is_available = False
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the bot with API keys/credentials
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    def chat_complete(self, messages: List[Dict[str, str]], model: str = None) -> str:
        """
        Send chat completion request
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Optional model name override
            
        Returns:
            str: Bot's response text
        """
        pass
    
    @property
    def is_available(self) -> bool:
        """Check if bot is available/initialized"""
        return self._is_available
    
    def get_display_name(self) -> str:
        """Get display name for UI"""
        return self.name
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the bot's model
        
        Returns:
            dict: Model metadata (name, capabilities, etc.)
        """
        return {
            "name": self.name,
            "available": self.is_available
        }
