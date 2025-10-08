"""
Main application for Teams-Intercom Integration.
FastAPI server with webhook endpoints and integration logic.
"""

import json
from contextlib import asynccontextmanager
from typing import Any, Dict

import structlog
import uvicorn
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from config import config
from graph_client import GraphClient
from intercom_client import IntercomClient
from webhook_handler import WebhookHandler

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

# Global clients
graph_client = None
webhook_handler = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global graph_client, webhook_handler

    # Startup
    logger.info("Starting Teams-Intercom Integration")

    try:
        # Initialize Graph client
        graph_client = GraphClient()
        authenticated = await graph_client.authenticate()

        if not authenticated:
            logger.error("Failed to authenticate with Microsoft Graph")
            raise Exception("Microsoft Graph authentication failed")

        # Initialize webhook handler
        webhook_handler = WebhookHandler(graph_client, IntercomClient)

        logger.info("Application initialized successfully")

        yield

    except Exception as e:
        logger.error(f"Failed to initialize application: {str(e)}")
        raise

    finally:
        # Shutdown
        logger.info("Shutting down Teams-Intercom Integration")

        if graph_client:
            await graph_client.close()


# Create FastAPI app
app = FastAPI(
    title="Teams-Intercom Integration",
    description="Seamless integration between Microsoft Teams and Intercom FIN AI",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Teams-Intercom Integration",
        "version": "1.0.0",
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    health_status = {
        "status": "healthy",
        "timestamp": structlog.processors.TimeStamper()._make_stamper(
            "%Y-%m-%d %H:%M:%S"
        )(),
        "services": {
            "graph_api": graph_client._authenticated if graph_client else False,
            "webhook_handler": webhook_handler is not None,
        },
    }

    if not all(health_status["services"].values()):
        health_status["status"] = "degraded"

    return health_status


@app.post(config.webhook_path)
async def handle_intercom_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Handle incoming Intercom webhooks.

    Args:
        request: FastAPI request object
        background_tasks: Background task manager

    Returns:
        JSON response
    """
    try:
        # Get raw payload and signature
        payload = await request.body()
        signature = request.headers.get("X-Hub-Signature-256", "")

        # Verify webhook signature
        if not webhook_handler.verify_webhook_signature(payload, signature):
            logger.error("Invalid webhook signature")
            raise HTTPException(status_code=401, detail="Invalid signature")

        # Parse JSON payload
        try:
            data = json.loads(payload.decode("utf-8"))
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON payload: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid JSON payload")

        # Extract event type
        topic = data.get("topic")
        if not topic:
            logger.error("Missing topic in webhook data")
            raise HTTPException(status_code=400, detail="Missing topic")

        # Log webhook received
        logger.info(f"Received webhook: {topic}")

        # Process webhook in background
        background_tasks.add_task(process_webhook_background, topic, data)

        return JSONResponse(
            status_code=200, content={"status": "accepted", "topic": topic}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def process_webhook_background(event_type: str, data: Dict[str, Any]):
    """
    Process webhook in background task.

    Args:
        event_type: Type of webhook event
        data: Webhook data
    """
    try:
        result = await webhook_handler.process_webhook(event_type, data)
        logger.info(f"Webhook processed successfully: {result}")

    except Exception as e:
        logger.error(f"Background webhook processing failed: {str(e)}")


@app.get("/teams")
async def get_teams():
    """Get all Teams the bot has access to."""
    try:
        if not graph_client or not graph_client._authenticated:
            raise HTTPException(
                status_code=401, detail="Not authenticated with Microsoft Graph"
            )

        teams = await graph_client.get_teams()
        return {"teams": teams, "count": len(teams)}

    except Exception as e:
        logger.error(f"Failed to get teams: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/teams/{team_id}/channels")
async def get_team_channels(team_id: str):
    """Get channels for a specific team."""
    try:
        if not graph_client or not graph_client._authenticated:
            raise HTTPException(
                status_code=401, detail="Not authenticated with Microsoft Graph"
            )

        channels = await graph_client.get_team_channels(team_id)
        return {"channels": channels, "count": len(channels)}

    except Exception as e:
        logger.error(f"Failed to get channels for team {team_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/teams/{team_id}/channels")
async def create_channel(team_id: str, channel_data: Dict[str, str]):
    """Create a new channel in a team."""
    try:
        if not graph_client or not graph_client._authenticated:
            raise HTTPException(
                status_code=401, detail="Not authenticated with Microsoft Graph"
            )

        channel_name = channel_data.get("name")
        description = channel_data.get("description", "")

        if not channel_name:
            raise HTTPException(status_code=400, detail="Channel name is required")

        channel = await graph_client.create_channel(team_id, channel_name, description)
        return {"channel": channel}

    except Exception as e:
        logger.error(f"Failed to create channel in team {team_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/teams/{team_id}/channels/{channel_id}/messages")
async def send_message(team_id: str, channel_id: str, message_data: Dict[str, str]):
    """Send a message to a Teams channel."""
    try:
        if not graph_client or not graph_client._authenticated:
            raise HTTPException(
                status_code=401, detail="Not authenticated with Microsoft Graph"
            )

        message = message_data.get("message")
        message_type = message_data.get("type", "html")

        if not message:
            raise HTTPException(status_code=400, detail="Message content is required")

        sent_message = await graph_client.send_message(
            team_id, channel_id, message, message_type
        )
        return {"message": sent_message}

    except Exception as e:
        logger.error(
            f"Failed to send message to team {team_id}, channel {channel_id}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/teams/{team_id}/channels/{channel_id}/messages")
async def get_channel_messages(team_id: str, channel_id: str, limit: int = 50):
    """Get messages from a Teams channel."""
    try:
        if not graph_client or not graph_client._authenticated:
            raise HTTPException(
                status_code=401, detail="Not authenticated with Microsoft Graph"
            )

        messages = await graph_client.get_channel_messages(team_id, channel_id, limit)
        return {"messages": messages, "count": len(messages)}

    except Exception as e:
        logger.error(
            f"Failed to get messages from team {team_id}, "
            f"channel {channel_id}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/intercom/conversations")
async def get_intercom_conversations(limit: int = 20):
    """Get recent Intercom conversations."""
    try:
        async with IntercomClient() as client:
            conversations = await client.get_conversations(limit)

        return {"conversations": conversations, "count": len(conversations)}

    except Exception as e:
        logger.error(f"Failed to get Intercom conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sync/conversation-to-teams")
async def sync_conversation_to_teams(sync_data: Dict[str, Any]):
    """Manually sync an Intercom conversation to Teams."""
    try:
        conversation_id = sync_data.get("conversation_id")
        team_id = sync_data.get("team_id", config.default_team_id)

        if not conversation_id:
            raise HTTPException(status_code=400, detail="Conversation ID is required")

        if not team_id:
            raise HTTPException(status_code=400, detail="Team ID is required")

        # Get conversation details from Intercom
        async with IntercomClient() as client:
            conversation = await client.get_conversation(conversation_id)

        # Format message for Teams
        user = conversation.get("source", {}).get("author", {})
        user_name = user.get("name", "Unknown User")
        user_email = user.get("email", "No email")

        parts = conversation.get("conversation_parts", {}).get("conversation_parts", [])
        latest_message = "No message content"
        if parts:
            latest_message = parts[-1].get("body", "No message content")

        teams_message = f"""
🔄 **Manual Sync - Conversation {conversation_id}**

**Customer:** {user_name} ({user_email})
**Latest Message:**
{latest_message}

[View in Intercom](https://app.intercom.com/a/apps/{conversation_id})
"""

        # Send to Teams
        channel = await graph_client.find_or_create_channel(
            team_id,
            config.default_channel_name,
            "Customer support inquiries from Intercom",
        )

        sent_message = await graph_client.send_message(
            team_id, channel["id"], teams_message, "html"
        )

        return {
            "status": "success",
            "conversation_id": conversation_id,
            "teams_message": sent_message,
        }

    except Exception as e:
        logger.error(
            f"Failed to sync conversation {sync_data.get('conversation_id')}: {str(e)}"
        )
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/teams/message-from-intercom")
async def forward_teams_message_to_intercom(message_data: Dict[str, Any]):
    """Forward a Teams message to create/update an Intercom conversation."""
    try:
        teams_message = message_data.get("message")
        user_email = message_data.get("user_email")
        conversation_id = message_data.get("conversation_id")  # Optional

        if not teams_message or not user_email:
            raise HTTPException(
                status_code=400, detail="Message and user email are required"
            )

        async with IntercomClient() as client:
            if conversation_id:
                # Reply to existing conversation
                result = await client.reply_to_conversation(
                    conversation_id, teams_message, "comment"
                )
            else:
                # Create new conversation or find/create user first
                user_data = {"email": user_email, "role": "user"}
                user = await client.create_or_update_user(user_data)

                result = await client.create_conversation(
                    user["id"], teams_message, "comment"
                )

        return {
            "status": "success",
            "action": "message_forwarded",
            "intercom_response": result,
        }

    except Exception as e:
        logger.error(f"Failed to forward Teams message to Intercom: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.host,
        port=config.port,
        reload=config.debug,
        log_level="info",
    )
