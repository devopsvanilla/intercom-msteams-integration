"""
Webhook handler for Intercom events and Teams integration.
Processes incoming webhooks and triggers appropriate actions.
"""

import hashlib
import hmac
import logging
from datetime import datetime
from typing import Any, Dict

from fastapi import HTTPException

from config import config

logger = logging.getLogger(__name__)


class WebhookHandler:
    """Handles Intercom webhooks and processes events."""

    def __init__(self, graph_client, intercom_client):
        """
        Initialize webhook handler.

        Args:
            graph_client: Microsoft Graph client instance
            intercom_client: Intercom client instance
        """
        self.graph_client = graph_client
        self.intercom_client = intercom_client
        self.webhook_secret = config.intercom.webhook_secret

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verify Intercom webhook signature.

        Args:
            payload (bytes): Raw webhook payload
            signature (str): Webhook signature from headers

        Returns:
            bool: True if signature is valid
        """
        if not self.webhook_secret:
            logger.warning(
                "Webhook secret not configured, skipping signature verification"
            )
            return True

        try:
            # Remove 'sha256=' prefix if present
            if signature.startswith("sha256="):
                signature = signature[7:]

            # Calculate expected signature
            expected_signature = hmac.new(
                self.webhook_secret.encode("utf-8"), payload, hashlib.sha256
            ).hexdigest()

            # Compare signatures
            is_valid = hmac.compare_digest(expected_signature, signature)

            if not is_valid:
                logger.error("Invalid webhook signature")

            return is_valid

        except Exception as e:
            logger.error(f"Error verifying webhook signature: {str(e)}")
            return False

    async def process_webhook(
        self, event_type: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process incoming webhook event.

        Args:
            event_type (str): Type of webhook event
            data (Dict): Event data

        Returns:
            Dict: Processing result
        """
        try:
            logger.info(f"Processing webhook event: {event_type}")

            # Route to appropriate handler based on event type
            if event_type == "conversation.user.created":
                return await self._handle_conversation_created(data)
            elif event_type == "conversation.user.replied":
                return await self._handle_conversation_reply(data)
            elif event_type == "conversation.admin.replied":
                return await self._handle_admin_reply(data)
            elif event_type == "conversation.admin.assigned":
                return await self._handle_conversation_assigned(data)
            elif event_type == "conversation.admin.closed":
                return await self._handle_conversation_closed(data)
            else:
                logger.info(f"Unhandled event type: {event_type}")
                return {"status": "ignored", "event_type": event_type}

        except Exception as e:
            logger.error(f"Error processing webhook {event_type}: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Webhook processing failed: {str(e)}"
            )

    async def _handle_conversation_created(
        self, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle new conversation created event.

        Args:
            data (Dict): Event data

        Returns:
            Dict: Processing result
        """
        try:
            conversation = data.get("data", {}).get("item", {})
            conversation_id = conversation.get("id")

            if not conversation_id:
                logger.error("No conversation ID in webhook data")
                return {"status": "error", "message": "Missing conversation ID"}

            # Get conversation details
            async with self.intercom_client as client:
                conversation_details = await client.get_conversation(conversation_id)

            # Extract relevant information
            user = conversation_details.get("source", {}).get("author", {})
            user_name = user.get("name", "Unknown User")
            user_email = user.get("email", "No email")

            # Get the first message
            parts = conversation_details.get("conversation_parts", {}).get(
                "conversation_parts", []
            )
            first_message = "No message content"
            if parts and len(parts) > 0:
                first_message = parts[0].get("body", "No message content")

            # Create Teams message
            teams_message = f"""
🔔 **New Customer Inquiry**

**Customer:** {user_name} ({user_email})
**Conversation ID:** {conversation_id}
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Message:**
{first_message}

[View in Intercom](https://app.intercom.com/a/apps/{conversation_id})
"""

            # Send to default Teams channel
            if config.default_team_id:
                channel = await self.graph_client.find_or_create_channel(
                    config.default_team_id,
                    config.default_channel_name,
                    "Customer support inquiries from Intercom",
                )

                await self.graph_client.send_message(
                    config.default_team_id, channel["id"], teams_message, "html"
                )

                logger.info(
                    f"Sent new conversation notification to Teams for {conversation_id}"
                )

            return {
                "status": "success",
                "action": "conversation_created_notification",
                "conversation_id": conversation_id,
            }

        except Exception as e:
            logger.error(f"Error handling conversation created: {str(e)}")
            raise

    async def _handle_conversation_reply(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle user reply in conversation.

        Args:
            data (Dict): Event data

        Returns:
            Dict: Processing result
        """
        try:
            conversation = data.get("data", {}).get("item", {})
            conversation_id = conversation.get("id")

            if not conversation_id:
                return {"status": "error", "message": "Missing conversation ID"}

            # Get latest conversation part
            async with self.intercom_client as client:
                parts = await client.get_conversation_parts(conversation_id)

                if not parts:
                    return {"status": "error", "message": "No conversation parts found"}

                latest_part = parts[-1]  # Get the most recent part
                message_body = latest_part.get("body", "")
                latest_part.get("author", {})

                # Try to trigger FIN AI response
                fin_response = await client.trigger_fin_ai_response(
                    conversation_id, message_body
                )

            # Create Teams notification
            teams_message = f"""
💬 **Customer Reply - Conversation {conversation_id}**

**Customer Message:**
{message_body}

**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

            # Add FIN AI suggestion if available
            if fin_response:
                suggested_reply = fin_response.get("suggested_reply", "")
                if suggested_reply:
                    teams_message += f"""

🤖 **FIN AI Suggested Response:**
{suggested_reply}
"""

            intercom_url = f"https://app.intercom.com/a/apps/{conversation_id}"
            teams_message += f"\n[View in Intercom]({intercom_url})"

            # Send to Teams
            if config.default_team_id:
                channel = await self.graph_client.find_or_create_channel(
                    config.default_team_id, config.default_channel_name
                )

                await self.graph_client.send_message(
                    config.default_team_id, channel["id"], teams_message, "html"
                )

            return {
                "status": "success",
                "action": "user_reply_notification",
                "conversation_id": conversation_id,
                "fin_ai_used": fin_response is not None,
            }

        except Exception as e:
            logger.error(f"Error handling conversation reply: {str(e)}")
            raise

    async def _handle_admin_reply(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle admin reply in conversation.

        Args:
            data (Dict): Event data

        Returns:
            Dict: Processing result
        """
        try:
            conversation = data.get("data", {}).get("item", {})
            conversation_id = conversation.get("id")

            # For admin replies, we might want to sync back to Teams or just log
            logger.info(f"Admin replied to conversation {conversation_id}")

            return {
                "status": "success",
                "action": "admin_reply_logged",
                "conversation_id": conversation_id,
            }

        except Exception as e:
            logger.error(f"Error handling admin reply: {str(e)}")
            raise

    async def _handle_conversation_assigned(
        self, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle conversation assignment event.

        Args:
            data (Dict): Event data

        Returns:
            Dict: Processing result
        """
        try:
            conversation = data.get("data", {}).get("item", {})
            conversation_id = conversation.get("id")

            assignee = conversation.get("assignee", {})
            assignee_name = assignee.get("name", "Unknown")

            # Notify Teams about assignment
            teams_message = f"""
👤 **Conversation Assigned**

**Conversation ID:** {conversation_id}
**Assigned to:** {assignee_name}
**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

[View in Intercom](https://app.intercom.com/a/apps/{conversation_id})
"""

            if config.default_team_id:
                channel = await self.graph_client.find_or_create_channel(
                    config.default_team_id, config.default_channel_name
                )

                await self.graph_client.send_message(
                    config.default_team_id, channel["id"], teams_message, "html"
                )

            return {
                "status": "success",
                "action": "assignment_notification",
                "conversation_id": conversation_id,
                "assignee": assignee_name,
            }

        except Exception as e:
            logger.error(f"Error handling conversation assignment: {str(e)}")
            raise

    async def _handle_conversation_closed(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle conversation closed event.

        Args:
            data (Dict): Event data

        Returns:
            Dict: Processing result
        """
        try:
            conversation = data.get("data", {}).get("item", {})
            conversation_id = conversation.get("id")

            # Notify Teams about closure
            teams_message = f"""
✅ **Conversation Closed**

**Conversation ID:** {conversation_id}
**Closed at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

[View in Intercom](https://app.intercom.com/a/apps/{conversation_id})
"""

            if config.default_team_id:
                channel = await self.graph_client.find_or_create_channel(
                    config.default_team_id, config.default_channel_name
                )

                await self.graph_client.send_message(
                    config.default_team_id, channel["id"], teams_message, "html"
                )

            return {
                "status": "success",
                "action": "closure_notification",
                "conversation_id": conversation_id,
            }

        except Exception as e:
            logger.error(f"Error handling conversation closure: {str(e)}")
            raise
