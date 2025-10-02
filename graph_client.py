"""
Microsoft Graph API client for Teams integration.
Handles authentication, teams, channels, and message operations.
"""

import asyncio
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime

from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.models.team import Team
from msgraph.generated.models.channel import Channel
from msgraph.generated.models.chat_message import ChatMessage
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType

from config import config

logger = logging.getLogger(__name__)


class GraphClient:
    """Microsoft Graph API client for Teams operations."""
    
    def __init__(self):
        self.credential = None
        self.client = None
        self._authenticated = False
    
    async def authenticate(self) -> bool:
        """
        Authenticate with Azure AD using client credentials flow.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            self.credential = ClientSecretCredential(
                tenant_id=config.azure.tenant_id,
                client_id=config.azure.client_id,
                client_secret=config.azure.client_secret
            )
            
            self.client = GraphServiceClient(
                credentials=self.credential,
                scopes=config.azure.scopes
            )
            
            # Test authentication by getting current user
            await self.client.me.get()
            self._authenticated = True
            logger.info("Successfully authenticated with Microsoft Graph")
            return True
            
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            self._authenticated = False
            return False
    
    async def get_teams(self) -> List[Dict[str, Any]]:
        """
        Get all teams the authenticated user has access to.
        
        Returns:
            List[Dict]: List of team objects with id, displayName, description
        """
        if not self._authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        try:
            teams_response = await self.client.me.joined_teams.get()
            teams = []
            
            if teams_response and teams_response.value:
                for team in teams_response.value:
                    teams.append({
                        'id': team.id,
                        'displayName': team.display_name,
                        'description': team.description or '',
                        'createdDateTime': team.created_date_time.isoformat() if team.created_date_time else None
                    })
            
            logger.info(f"Retrieved {len(teams)} teams")
            return teams
            
        except Exception as e:
            logger.error(f"Failed to get teams: {str(e)}")
            raise
    
    async def get_team_channels(self, team_id: str) -> List[Dict[str, Any]]:
        """
        Get all channels for a specific team.
        
        Args:
            team_id (str): The team ID
            
        Returns:
            List[Dict]: List of channel objects
        """
        if not self._authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        try:
            channels_response = await self.client.teams.by_team_id(team_id).channels.get()
            channels = []
            
            if channels_response and channels_response.value:
                for channel in channels_response.value:
                    channels.append({
                        'id': channel.id,
                        'displayName': channel.display_name,
                        'description': channel.description or '',
                        'membershipType': channel.membership_type.value if channel.membership_type else 'standard',
                        'createdDateTime': channel.created_date_time.isoformat() if channel.created_date_time else None
                    })
            
            logger.info(f"Retrieved {len(channels)} channels for team {team_id}")
            return channels
            
        except Exception as e:
            logger.error(f"Failed to get channels for team {team_id}: {str(e)}")
            raise
    
    async def create_channel(self, team_id: str, channel_name: str, description: str = "") -> Dict[str, Any]:
        """
        Create a new channel in a team.
        
        Args:
            team_id (str): The team ID
            channel_name (str): Name of the new channel
            description (str): Channel description
            
        Returns:
            Dict: Created channel object
        """
        if not self._authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        try:
            channel = Channel(
                display_name=channel_name,
                description=description
            )
            
            created_channel = await self.client.teams.by_team_id(team_id).channels.post(channel)
            
            result = {
                'id': created_channel.id,
                'displayName': created_channel.display_name,
                'description': created_channel.description or '',
                'membershipType': created_channel.membership_type.value if created_channel.membership_type else 'standard'
            }
            
            logger.info(f"Created channel '{channel_name}' in team {team_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to create channel '{channel_name}' in team {team_id}: {str(e)}")
            raise
    
    async def send_message(self, team_id: str, channel_id: str, message: str, message_type: str = "html") -> Dict[str, Any]:
        """
        Send a message to a Teams channel.
        
        Args:
            team_id (str): The team ID
            channel_id (str): The channel ID
            message (str): Message content
            message_type (str): Message type (html or text)
            
        Returns:
            Dict: Sent message object
        """
        if not self._authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        try:
            body_type = BodyType.Html if message_type.lower() == "html" else BodyType.Text
            
            chat_message = ChatMessage(
                body=ItemBody(
                    content_type=body_type,
                    content=message
                )
            )
            
            sent_message = await self.client.teams.by_team_id(team_id).channels.by_channel_id(channel_id).messages.post(chat_message)
            
            result = {
                'id': sent_message.id,
                'content': sent_message.body.content if sent_message.body else message,
                'createdDateTime': sent_message.created_date_time.isoformat() if sent_message.created_date_time else None,
                'from': sent_message.from_property.user.display_name if sent_message.from_property and sent_message.from_property.user else 'Bot'
            }
            
            logger.info(f"Sent message to team {team_id}, channel {channel_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to send message to team {team_id}, channel {channel_id}: {str(e)}")
            raise
    
    async def get_channel_messages(self, team_id: str, channel_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent messages from a channel.
        
        Args:
            team_id (str): The team ID
            channel_id (str): The channel ID
            limit (int): Maximum number of messages to retrieve
            
        Returns:
            List[Dict]: List of message objects
        """
        if not self._authenticated:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        try:
            messages_response = await self.client.teams.by_team_id(team_id).channels.by_channel_id(channel_id).messages.get()
            messages = []
            
            if messages_response and messages_response.value:
                for message in messages_response.value[:limit]:
                    messages.append({
                        'id': message.id,
                        'content': message.body.content if message.body else '',
                        'contentType': message.body.content_type.value if message.body and message.body.content_type else 'text',
                        'createdDateTime': message.created_date_time.isoformat() if message.created_date_time else None,
                        'from': message.from_property.user.display_name if message.from_property and message.from_property.user else 'Unknown'
                    })
            
            logger.info(f"Retrieved {len(messages)} messages from team {team_id}, channel {channel_id}")
            return messages
            
        except Exception as e:
            logger.error(f"Failed to get messages from team {team_id}, channel {channel_id}: {str(e)}")
            raise
    
    async def find_or_create_channel(self, team_id: str, channel_name: str, description: str = "") -> Dict[str, Any]:
        """
        Find an existing channel or create a new one.
        
        Args:
            team_id (str): The team ID
            channel_name (str): Channel name to find or create
            description (str): Description for new channel
            
        Returns:
            Dict: Channel object (existing or newly created)
        """
        try:
            # First, try to find existing channel
            channels = await self.get_team_channels(team_id)
            
            for channel in channels:
                if channel['displayName'].lower() == channel_name.lower():
                    logger.info(f"Found existing channel '{channel_name}' in team {team_id}")
                    return channel
            
            # Channel not found, create new one
            logger.info(f"Channel '{channel_name}' not found, creating new one in team {team_id}")
            return await self.create_channel(team_id, channel_name, description)
            
        except Exception as e:
            logger.error(f"Failed to find or create channel '{channel_name}' in team {team_id}: {str(e)}")
            raise
    
    async def close(self):
        """Clean up resources."""
        if self.credential:
            await self.credential.close()
        self._authenticated = False
        logger.info("Graph client closed")