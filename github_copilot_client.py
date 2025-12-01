#!/usr/bin/env python3
"""
GitHub Copilot API Client
Provides interface to GitHub Copilot Chat API using GitHub credentials
"""

import os
import requests
from typing import List, Dict, Optional


class GitHubCopilotClient:
    """Client for interacting with GitHub Copilot API"""
    
    def __init__(self, github_token: str):
        """
        Initialize GitHub Copilot client
        
        Args:
            github_token: GitHub Personal Access Token with Copilot access
        """
        self.github_token = github_token
        self.base_url = "https://api.githubcopilot.com"
        self.headers = {
            "Authorization": f"Bearer {github_token}",
            "Content-Type": "application/json",
            "Editor-Version": "vscode/1.85.0",
            "Editor-Plugin-Version": "copilot-chat/0.11.0",
            "User-Agent": "GitHubCopilotChat/0.11.0"
        }
    
    def chat_complete(self, messages: List[Dict[str, str]], model: str = "gpt-4") -> Dict:
        """
        Send chat completion request to GitHub Copilot
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            model: Model to use (gpt-4 or gpt-3.5-turbo)
            
        Returns:
            Response dictionary with choices containing the assistant's message
        """
        endpoint = f"{self.base_url}/chat/completions"
        
        payload = {
            "messages": messages,
            "model": model,
            "temperature": 0.7,
            "top_p": 1,
            "n": 1,
            "stream": False
        }
        
        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            # Fallback: If GitHub Copilot API is not available, use standard OpenAI-compatible endpoint
            # Some GitHub enterprise setups use different endpoints
            return self._fallback_chat_complete(messages, model)
    
    def _fallback_chat_complete(self, messages: List[Dict[str, str]], model: str) -> Dict:
        """
        Fallback method using standard GitHub Models API
        This works with standard GitHub tokens
        """
        # GitHub Models API endpoint (available to GitHub users)
        endpoint = "https://models.inference.ai.azure.com/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "messages": messages,
            "model": "gpt-4o",  # GitHub Models supports various models
            "temperature": 0.7,
            "max_tokens": 4096,
            "top_p": 1
        }
        
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            # If all else fails, return error in expected format
            return {
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": f"Error communicating with GitHub API: {str(e)}\n\nPlease ensure your GitHub token has proper permissions."
                    }
                }]
            }


class MockCopilotResponse:
    """Mock response object to match Mistral AI interface"""
    
    def __init__(self, content: str):
        self.choices = [MockChoice(content)]


class MockChoice:
    """Mock choice object"""
    
    def __init__(self, content: str):
        self.message = MockMessage(content)


class MockMessage:
    """Mock message object"""
    
    def __init__(self, content: str):
        self.content = content


class GitHubCopilotAdapter:
    """
    Adapter to make GitHub Copilot client compatible with Mistral AI interface
    This allows drop-in replacement in existing code
    """
    
    def __init__(self, github_token: str):
        self.client = GitHubCopilotClient(github_token)
    
    class ChatCompletions:
        """Nested class to match Mistral's client.chat interface"""
        
        def __init__(self, client: GitHubCopilotClient):
            self.client = client
        
        def complete(self, model: str, messages: List[Dict[str, str]]) -> MockCopilotResponse:
            """
            Complete chat request - matches Mistral AI interface
            
            Args:
                model: Model name (will be mapped to GitHub Copilot models)
                messages: List of message dictionaries
                
            Returns:
                Response object with .choices[0].message.content
            """
            # Map Mistral model names to GitHub Copilot models
            model_mapping = {
                "mistral-small-latest": "gpt-4o",
                "mistral-medium-latest": "gpt-4o",
                "mistral-large-latest": "gpt-4o",
            }
            
            github_model = model_mapping.get(model, "gpt-4o")
            
            response = self.client.chat_complete(messages, github_model)
            
            # Extract content from response
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "No response")
            
            return MockCopilotResponse(content)
    
    @property
    def chat(self):
        """Property to match Mistral's client.chat interface"""
        return self.ChatCompletions(self.client)


# Factory function for easy integration
def create_copilot_client(github_token: Optional[str] = None) -> GitHubCopilotAdapter:
    """
    Create GitHub Copilot client with Mistral-compatible interface
    
    Args:
        github_token: GitHub Personal Access Token (if None, reads from env)
        
    Returns:
        GitHubCopilotAdapter instance
    """
    if github_token is None:
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("GITHUB_TOKEN not found in environment or parameters")
    
    return GitHubCopilotAdapter(github_token)
