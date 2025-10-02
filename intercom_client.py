"""
Intercom API client for FIN AI integration.
Handles conversations, tickets, and AI responses.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
import aiohttp
import json
from datetime import datetime

from config import config

logger = logging.getLogger(__name__)


class IntercomClient:
    """Intercom API client for FIN AI integration."""
    
    def __init__(self):
        self.base_url = config.intercom.base_url
        self.access_token = config.intercom.access_token
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            headers={
                'Authorization': f'Bearer {self.access_token}',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make HTTP request to Intercom API.
        
        Args:
            method (str): HTTP method
            endpoint (str): API endpoint
            data (Optional[Dict]): Request payload
            
        Returns:
            Dict: API response
        """
        if not self.session:
            raise Exception("Client not initialized. Use async context manager.")
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            async with self.session.request(method, url, json=data) as response:
                response_data = await response.json()
                
                if response.status >= 400:
                    logger.error(f"Intercom API error {response.status}: {response_data}")
                    raise Exception(f"Intercom API error: {response_data.get('errors', [{}])[0].get('message', 'Unknown error')}")
                
                return response_data
                
        except aiohttp.ClientError as e:
            logger.error(f"HTTP client error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise
    
    async def get_conversations(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get recent conversations.
        
        Args:
            limit (int): Maximum number of conversations to retrieve
            
        Returns:
            List[Dict]: List of conversation objects
        """
        try:
            response = await self._make_request('GET', f'/conversations?per_page={limit}')
            conversations = response.get('conversations', [])
            
            logger.info(f"Retrieved {len(conversations)} conversations")
            return conversations
            
        except Exception as e:
            logger.error(f"Failed to get conversations: {str(e)}")
            raise
    
    async def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get a specific conversation by ID.
        
        Args:
            conversation_id (str): The conversation ID
            
        Returns:
            Dict: Conversation object
        """
        try:
            response = await self._make_request('GET', f'/conversations/{conversation_id}')
            
            logger.info(f"Retrieved conversation {conversation_id}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to get conversation {conversation_id}: {str(e)}")
            raise
    
    async def create_conversation(self, user_id: str, body: str, message_type: str = "comment") -> Dict[str, Any]:
        """
        Create a new conversation.
        
        Args:
            user_id (str): User ID to create conversation for
            body (str): Message body
            message_type (str): Message type (comment, note, etc.)
            
        Returns:
            Dict: Created conversation object
        """
        try:
            data = {
                "from": {
                    "type": "user",
                    "id": user_id
                },
                "body": body,
                "message_type": message_type
            }
            
            response = await self._make_request('POST', '/conversations', data)
            
            logger.info(f"Created conversation for user {user_id}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to create conversation for user {user_id}: {str(e)}")
            raise
    
    async def reply_to_conversation(self, conversation_id: str, body: str, message_type: str = "comment", admin_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Reply to an existing conversation.
        
        Args:
            conversation_id (str): The conversation ID
            body (str): Reply message body
            message_type (str): Message type
            admin_id (Optional[str]): Admin ID if replying as admin
            
        Returns:
            Dict: Reply object
        """
        try:
            data = {
                "message_type": message_type,
                "body": body
            }
            
            if admin_id:
                data["admin_id"] = admin_id
            
            response = await self._make_request('POST', f'/conversations/{conversation_id}/reply', data)
            
            logger.info(f"Replied to conversation {conversation_id}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to reply to conversation {conversation_id}: {str(e)}")
            raise
    
    async def search_conversations(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search conversations using Intercom's search API.
        
        Args:
            query (str): Search query
            limit (int): Maximum results
            
        Returns:
            List[Dict]: Search results
        """
        try:
            data = {
                "query": {
                    "operator": "AND",
                    "value": [
                        {
                            "field": "conversation_parts.body",
                            "operator": "~",
                            "value": query
                        }
                    ]
                },
                "pagination": {
                    "per_page": limit
                }
            }
            
            response = await self._make_request('POST', '/conversations/search', data)
            conversations = response.get('conversations', [])
            
            logger.info(f"Found {len(conversations)} conversations matching '{query}'")
            return conversations
            
        except Exception as e:
            logger.error(f"Failed to search conversations: {str(e)}")
            raise
    
    async def get_conversation_parts(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Get all parts (messages) of a conversation.
        
        Args:
            conversation_id (str): The conversation ID
            
        Returns:
            List[Dict]: List of conversation parts
        """
        try:
            conversation = await self.get_conversation(conversation_id)
            parts = conversation.get('conversation_parts', {}).get('conversation_parts', [])
            
            logger.info(f"Retrieved {len(parts)} parts for conversation {conversation_id}")
            return parts
            
        except Exception as e:
            logger.error(f"Failed to get conversation parts for {conversation_id}: {str(e)}")
            raise
    
    async def trigger_fin_ai_response(self, conversation_id: str, query: str) -> Optional[Dict[str, Any]]:
        """
        Trigger FIN AI to generate a response for a conversation.
        
        Args:
            conversation_id (str): The conversation ID
            query (str): Query to send to FIN AI
            
        Returns:
            Optional[Dict]: FIN AI response if available
        """
        try:
            # Note: This is a placeholder for FIN AI integration
            # The actual implementation would depend on Intercom's FIN AI API
            # which may require special access or different endpoints
            
            data = {
                "conversation_id": conversation_id,
                "query": query,
                "ai_model": "fin"
            }
            
            # This endpoint might be different in the actual Intercom FIN AI API
            response = await self._make_request('POST', '/conversations/ai/suggest', data)
            
            logger.info(f"Generated FIN AI response for conversation {conversation_id}")
            return response
            
        except Exception as e:
            logger.warning(f"FIN AI response not available for conversation {conversation_id}: {str(e)}")
            return None
    
    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Get user information by ID.
        
        Args:
            user_id (str): The user ID
            
        Returns:
            Dict: User object
        """
        try:
            response = await self._make_request('GET', f'/users/{user_id}')
            
            logger.info(f"Retrieved user {user_id}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to get user {user_id}: {str(e)}")
            raise
    
    async def create_or_update_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create or update a user.
        
        Args:
            user_data (Dict): User data including email, name, etc.
            
        Returns:
            Dict: User object
        """
        try:
            response = await self._make_request('POST', '/users', user_data)
            
            logger.info(f"Created/updated user {user_data.get('email', user_data.get('user_id'))}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to create/update user: {str(e)}")
            raise