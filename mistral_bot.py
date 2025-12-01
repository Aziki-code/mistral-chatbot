#!/usr/bin/env python3
"""
Mistral AI Bot
Handles all Mistral AI specific logic and API communication
"""

import os
from typing import List, Dict, Optional
from base_bot import BaseBot


class MistralBot(BaseBot):
    """Mistral AI chatbot implementation"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Mistral bot
        
        Args:
            api_key: Mistral API key (if None, reads from env)
        """
        super().__init__("Mistral AI")
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        self.client = None
        self.default_model = "mistral-small-latest"
        
        # Try to initialize immediately
        self.initialize()
    
    def initialize(self) -> bool:
        """
        Initialize Mistral AI client
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.api_key:
            self._is_available = False
            return False
        
        try:
            from mistralai.client import MistralClient
            from mistralai.models.chat_completion import ChatMessage
            self.client = MistralClient(api_key=self.api_key)
            self._is_available = True
            return True
        except ImportError:
            self._is_available = False
            return False
        except Exception as e:
            self._is_available = False
            return False
    
    def chat_complete(self, messages: List[Dict[str, str]], model: str = None) -> str:
        """
        Send chat completion request to Mistral AI
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (uses default if None)
            
        Returns:
            str: Bot's response text
            
        Raises:
            RuntimeError: If bot is not initialized
        """
        if not self.is_available:
            raise RuntimeError(f"{self.name} is not available. Check API key.")
        
        try:
            model_name = model or self.default_model
            
            from mistralai.models.chat_completion import ChatMessage
            
            # Convert dict messages to ChatMessage objects
            messages_objs = [
                ChatMessage(role=msg["role"], content=msg["content"])
                for msg in messages
            ]
            
            response = self.client.chat(
                model=model_name,
                messages=messages_objs
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            error_msg = f"Error communicating with {self.name}: {str(e)}"
            return f"❌ {error_msg}"
    
    def get_model_info(self) -> Dict[str, any]:
        """Get Mistral AI model information"""
        return {
            "name": self.name,
            "available": self.is_available,
            "default_model": self.default_model,
            "provider": "Mistral AI",
            "icon": "🤖",
            "supported_models": [
                "mistral-small-latest",
                "mistral-medium-latest",
                "mistral-large-latest"
            ]
        }
    
    def get_display_name(self) -> str:
        """Get display name for UI"""
        return "🤖 Mistral AI"
