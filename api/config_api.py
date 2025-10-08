import json
import os
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# Configuration file paths
CONFIG_FILE = ".env"  # For basic environment config
TEAMS_CONFIG_FILE = Path("config/teams_channels_config.json")  # For multi-teams config


# Pydantic models for basic config
class ConfigSettings(BaseModel):
    azure_client_id: Optional[str] = None
    azure_tenant_id: Optional[str] = None
    intercom_access_token: Optional[str] = None
    default_team_id: Optional[str] = None
    default_channel_name: Optional[str] = None


# Pydantic models for multi-teams config
class ChannelConfig(BaseModel):
    channel_name: str = Field(..., description="Name of the Teams channel")
    channel_id: Optional[str] = Field(None, description="Teams channel ID")
    intercom_tag: Optional[str] = Field(None, description="Intercom tag for routing")


class TeamConfig(BaseModel):
    team_name: str = Field(..., description="Name of the Teams team")
    team_id: str = Field(..., description="Teams team ID")
    channels: List[ChannelConfig] = Field(default_factory=list)


class TeamsChannelsConfig(BaseModel):
    teams: List[TeamConfig] = Field(default_factory=list)


# Router for multi-teams configuration
router = APIRouter(prefix="/api/config", tags=["configuration"])


@app.get("/api/config")
async def get_config():
    """Get current configuration settings from .env file"""
    try:
        config = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        config[key] = value
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/config")
async def update_config(settings: ConfigSettings):
    """Update configuration settings in .env file"""
    try:
        config_dict = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        config_dict[key] = value

        # Update with new values
        if settings.azure_client_id:
            config_dict["AZURE_CLIENT_ID"] = settings.azure_client_id
        if settings.azure_tenant_id:
            config_dict["AZURE_TENANT_ID"] = settings.azure_tenant_id
        if settings.intercom_access_token:
            config_dict["INTERCOM_ACCESS_TOKEN"] = settings.intercom_access_token
        if settings.default_team_id:
            config_dict["DEFAULT_TEAM_ID"] = settings.default_team_id
        if settings.default_channel_name:
            config_dict["DEFAULT_CHANNEL_NAME"] = settings.default_channel_name

        # Write back to file
        with open(CONFIG_FILE, "w") as f:
            for key, value in config_dict.items():
                f.write(f"{key}={value}\n")

        return {"status": "success", "message": "Configuration updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/teams")
async def get_teams_config():
    """Get multi-teams and channels configuration from JSON file"""
    try:
        if not TEAMS_CONFIG_FILE.exists():
            return {"teams": []}

        with open(TEAMS_CONFIG_FILE, "r") as f:
            config_data = json.load(f)
        return config_data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to read teams config: {str(e)}"
        )


@router.post("/teams")
async def update_teams_config(config: TeamsChannelsConfig):
    """Update multi-teams and channels configuration in JSON file"""
    try:
        # Ensure config directory exists
        TEAMS_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Write configuration to JSON file
        with open(TEAMS_CONFIG_FILE, "w") as f:
            json.dump(config.dict(), f, indent=2)

        return {"status": "success", "message": "Teams configuration updated"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update teams config: {str(e)}"
        )


@router.post("/teams/{team_id}/channels")
async def add_channel_to_team(team_id: str, channel: ChannelConfig):
    """Add a new channel to an existing team configuration"""
    try:
        config_data = {"teams": []}
        if TEAMS_CONFIG_FILE.exists():
            with open(TEAMS_CONFIG_FILE, "r") as f:
                config_data = json.load(f)

        # Find the team and add channel
        team_found = False
        for team in config_data["teams"]:
            if team["team_id"] == team_id:
                team["channels"].append(channel.dict())
                team_found = True
                break

        if not team_found:
            raise HTTPException(status_code=404, detail=f"Team {team_id} not found")

        # Write back to file
        with open(TEAMS_CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=2)

        return {"status": "success", "message": "Channel added to team"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Include the router for multi-teams endpoints
app.include_router(router)


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
