"""
Configuration management for Teams-Intercom integration.
Handles environment variables and secure credential storage.
"""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class AzureConfig(BaseSettings):
    """Azure AD and Microsoft Graph configuration."""

    client_id: str = Field(..., env="AZURE_CLIENT_ID")
    client_secret: str = Field(..., env="AZURE_CLIENT_SECRET")
    tenant_id: str = Field(..., env="AZURE_TENANT_ID")
    redirect_uri: str = Field(
        default="http://localhost:8000/auth/callback", env="AZURE_REDIRECT_URI"
    )

    # Microsoft Graph scopes
    scopes: list[str] = Field(
        default=[
            "User.Read",
            "Team.ReadWrite.All",
            "Channel.ReadWrite.All",
            "Chat.ReadWrite",
            "ChannelMessage.Send",
        ]
    )


class IntercomConfig(BaseSettings):
    """Intercom API configuration."""

    access_token: str = Field(..., env="INTERCOM_ACCESS_TOKEN")
    webhook_secret: str = Field(..., env="INTERCOM_WEBHOOK_SECRET")
    base_url: str = Field(default="https://api.intercom.io", env="INTERCOM_BASE_URL")


class AppConfig(BaseSettings):
    """Main application configuration."""

    # Server settings
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    debug: bool = Field(default=False, env="DEBUG")

    # Integration settings
    default_team_id: Optional[str] = Field(default=None, env="DEFAULT_TEAM_ID")
    default_channel_name: str = Field(
        default="Customer Support", env="DEFAULT_CHANNEL_NAME"
    )

    # Webhook settings
    webhook_path: str = Field(default="/webhooks/intercom", env="WEBHOOK_PATH")

    azure: AzureConfig = AzureConfig()
    intercom: IntercomConfig = IntercomConfig()

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global configuration instance
config = AppConfig()
