"""
Configuration management for Teams-Intercom integration.
Handles environment variables and secure credential storage.
"""

import json
import os
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from typing import Optional, Union

from pydantic import Field, PrivateAttr

try:
    # pydantic v2 uses a separate pydantic-settings package
    from pydantic_settings import BaseSettings, SettingsConfigDict
except Exception:
    # fallback for pydantic v1 where BaseSettings is in pydantic
    try:
        from pydantic import BaseSettings  # type: ignore

        SettingsConfigDict = dict  # type: ignore[assignment]
    except Exception as e:
        raise ImportError(
            "Could not import BaseSettings from pydantic_settings or pydantic; install "
            "'pydantic-settings' for pydantic v2 or ensure 'pydantic' is installed."
        ) from e

try:
    from dotenv import dotenv_values
except Exception:  # pragma: no cover - optional dependency

    def dotenv_values(_: str) -> dict[str, str]:
        return {}


# dotenv is not required because pydantic BaseSettings loads `.env` via Config.env_file


@dataclass(slots=True)
class AzureConfig:
    """Azure AD and Microsoft Graph configuration."""

    client_id: str
    client_secret: str
    tenant_id: str
    redirect_uri: str = "http://localhost:8000/auth/callback"
    scopes: list[str] = dataclass_field(
        default_factory=lambda: ["https://graph.microsoft.com/.default"]
    )


@dataclass(slots=True)
class IntercomConfig:
    """Intercom API configuration."""

    access_token: str
    webhook_secret: str
    base_url: str = "https://api.intercom.io"


def _split_csv(value: Union[str, list[str], tuple[str, ...], None]) -> list[str]:
    """Convert comma-separated strings into lists for list settings."""

    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return []


def _parse_list_like(value: str) -> list[str]:
    """Parse JSON arrays or fallback to comma-separated values."""

    stripped = value.strip()
    if not stripped:
        return []
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        return _split_csv(stripped)
    if isinstance(parsed, list):
        return _split_csv(parsed)
    return _split_csv(stripped)


class AppConfig(BaseSettings):
    """Main application configuration."""

    # Server settings
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    environment: str = Field(default="development", env="ENVIRONMENT")

    # Azure credentials
    azure_client_id: str = Field(..., env="AZURE_CLIENT_ID")
    azure_client_secret: str = Field(..., env="AZURE_CLIENT_SECRET")
    azure_tenant_id: str = Field(..., env="AZURE_TENANT_ID")
    azure_redirect_uri: str = Field(
        default="http://localhost:8000/auth/callback", env="AZURE_REDIRECT_URI"
    )
    azure_scopes_raw: Optional[str] = Field(default=None, env="AZURE_SCOPES")

    # Intercom credentials
    intercom_access_token: str = Field(..., env="INTERCOM_ACCESS_TOKEN")
    intercom_webhook_secret: str = Field(..., env="INTERCOM_WEBHOOK_SECRET")
    intercom_base_url: str = Field(
        default="https://api.intercom.io", env="INTERCOM_BASE_URL"
    )

    # Integration settings
    default_team_id: Optional[str] = Field(default=None, env="DEFAULT_TEAM_ID")
    default_channel_name: str = Field(
        default="Customer Support", env="DEFAULT_CHANNEL_NAME"
    )

    # Webhook settings
    webhook_path: str = Field(default="/webhooks/intercom", env="WEBHOOK_PATH")
    cors_origins_raw: Optional[str] = Field(default=None, env="CORS_ORIGINS")
    allowed_hosts_raw: Optional[str] = Field(default=None, env="ALLOWED_HOSTS")

    _cors_origins: list[str] = PrivateAttr(default_factory=list)
    _allowed_hosts: list[str] = PrivateAttr(default_factory=list)
    _azure: AzureConfig = PrivateAttr()
    _intercom: IntercomConfig = PrivateAttr()

    # Storage and cache
    config_store_path: str = Field(
        default="./config/teams_channels_config.json", env="CONFIG_STORE_PATH"
    )
    redis_host: Optional[str] = Field(default=None, env="REDIS_HOST")
    redis_port: Optional[int] = Field(default=None, env="REDIS_PORT")
    redis_password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    redis_db: int = Field(default=0, env="REDIS_DB")

    # TLS/SSL
    ssl_cert_path: Optional[str] = Field(default=None, env="SSL_CERT_PATH")
    ssl_key_path: Optional[str] = Field(default=None, env="SSL_KEY_PATH")

    # Monitoring
    sentry_dsn: Optional[str] = Field(default=None, env="SENTRY_DSN")
    enable_metrics: bool = Field(default=False, env="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, env="METRICS_PORT")

    def __init__(self, **data):
        super().__init__(**data)
        env_file = None
        if isinstance(self.model_config, dict):
            env_file = self.model_config.get("env_file")
        elif hasattr(self.model_config, "get"):  # SettingsConfigDict behaves like dict
            env_file = self.model_config.get("env_file")  # type: ignore[assignment]

        def _load_value(key: str, current: Optional[str]) -> str:
            if current:
                return current
            env_value = os.getenv(key)
            if env_value:
                return env_value
            if env_file:
                dotenv_value = dotenv_values(env_file).get(key)
                if dotenv_value:
                    return dotenv_value
            return ""

        cors_value = _load_value("CORS_ORIGINS", self.cors_origins_raw)
        hosts_value = _load_value("ALLOWED_HOSTS", self.allowed_hosts_raw)

        self._cors_origins = _parse_list_like(cors_value)
        self._allowed_hosts = _parse_list_like(hosts_value)
        azure_kwargs = {
            "client_id": self.azure_client_id,
            "client_secret": self.azure_client_secret,
            "tenant_id": self.azure_tenant_id,
            "redirect_uri": self.azure_redirect_uri,
        }
        if self.azure_scopes_raw:
            azure_kwargs["scopes"] = _parse_list_like(self.azure_scopes_raw)
        self._azure = AzureConfig(**azure_kwargs)
        self._intercom = IntercomConfig(
            access_token=self.intercom_access_token,
            webhook_secret=self.intercom_webhook_secret,
            base_url=self.intercom_base_url,
        )

    @property
    def cors_origins(self) -> list[str]:
        return list(self._cors_origins)

    @property
    def allowed_hosts(self) -> list[str]:
        return list(self._allowed_hosts)

    @property
    def azure(self) -> AzureConfig:
        return self._azure

    @property
    def intercom(self) -> IntercomConfig:
        return self._intercom

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


# Global configuration instance
config = AppConfig()
