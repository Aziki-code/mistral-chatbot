#!/usr/bin/env python3
"""
GitHub Copilot Bot
Handles all GitHub Copilot specific logic and API communication
"""

import os
import requests
from typing import List, Dict, Optional
from base_bot import BaseBot


class GitHubCopilotBot(BaseBot):
    """GitHub Copilot chatbot implementation"""
    
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize GitHub Copilot bot
        
        Args:
            github_token: GitHub Personal Access Token (if None, reads from env)
        """
        super().__init__("GitHub Copilot")
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        # Use GitHub Models API directly (works with PAT)
        self.base_url = "https://models.inference.ai.azure.com"
        self.default_model = "gpt-4o"
        
        # Try to initialize immediately
        self.initialize()
    
    def initialize(self) -> bool:
        """
        Initialize GitHub Copilot client
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.github_token:
            self._is_available = False
            return False
        
        try:
            # Validate token by making a test request
            self._is_available = True
            return True
        except Exception as e:
            self._is_available = False
            return False
    
    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for API requests"""
        return {
            "Authorization": f"Bearer {self.github_token}",
            "Content-Type": "application/json",
            "Editor-Version": "vscode/1.85.0",
            "Editor-Plugin-Version": "copilot-chat/0.11.0",
            "User-Agent": "GitHubCopilotChat/0.11.0"
        }
    
    def _map_model_name(self, model: str) -> str:
        """
        Map Mistral model names to GitHub Copilot models
        
        Args:
            model: Model name (potentially Mistral format)
            
        Returns:
            str: GitHub-compatible model name
        """
        model_mapping = {
            "mistral-small-latest": "gpt-4o",
            "mistral-medium-latest": "gpt-4o",
            "mistral-large-latest": "gpt-4o",
            "gpt-4": "gpt-4o",
            "gpt-3.5-turbo": "gpt-4o"
        }
        return model_mapping.get(model, self.default_model)
    
    def _chat_request(self, url: str, messages: List[Dict[str, str]], model: str) -> Optional[str]:
        """
        Make chat completion request to specific endpoint
        
        Args:
            url: API endpoint URL
            messages: Message history
            model: Model name
            
        Returns:
            str: Response text, or None if failed
        """
        payload = {
            "messages": messages,
            "model": model,
            "temperature": 0.7,
            "top_p": 1,
            "max_tokens": 4096
        }
        
        try:
            response = requests.post(
                f"{url}/chat/completions",
                headers=self._get_headers(),
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return None
    
    def chat_complete(self, messages: List[Dict[str, str]], model: str = None) -> str:
        """
        Send chat completion request to GitHub Models
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (uses default if None)
            
        Returns:
            str: Bot's response text
            
        Raises:
            RuntimeError: If bot is not initialized
        """
        if not self.is_available:
            raise RuntimeError(f"{self.name} is not available. Check GitHub token.")
        
        # Map model name to GitHub format
        github_model = self._map_model_name(model or self.default_model)
        
        # Use GitHub Models API directly
        result = self._chat_request(self.base_url, messages, github_model)
        if result:
            return result
        
        # Failed
        error_msg = f"{self.name} request failed. Check token permissions."
        return f"❌ {error_msg}"
    
    def get_model_info(self) -> Dict[str, any]:
        """Get GitHub Copilot model information"""
        return {
            "name": self.name,
            "available": self.is_available,
            "default_model": self.default_model,
            "provider": "GitHub/OpenAI",
            "icon": "💻",
            "supported_models": [
                "gpt-4o",
                "gpt-4-turbo",
                "gpt-3.5-turbo"
            ]
        }
    
    def get_display_name(self) -> str:
        """Get display name for UI"""
        return "💻 GitHub Copilot"
