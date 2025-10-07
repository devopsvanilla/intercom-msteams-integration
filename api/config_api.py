"""API endpoints for managing Teams and Channels configuration."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import json
import os
from pathlib import Path

router = APIRouter(prefix="/api/config", tags=["configuration"])

# Configuration file path
CONFIG_FILE = Path("config/teams_channels_config.json")

class ChannelConfig(BaseModel):
    """Channel configuration model."""
    channel_id: str = Field(..., description="Microsoft Teams Channel ID")
    channel_name: str = Field(..., description="Channel display name")
    
class TeamConfig(BaseModel):
    """Team configuration model."""
    team_id: str = Field(..., description="Microsoft Teams Team ID")
    team_name: str = Field(..., description="Team display name")
    channels: List[ChannelConfig] = Field(default_factory=list, description="List of channels")

class TeamsChannelsConfig(BaseModel):
    """Complete Teams and Channels configuration."""
    teams: List[TeamConfig] = Field(default_factory=list, description="List of configured teams")

def load_config() -> TeamsChannelsConfig:
    """Load configuration from file."""
    if not CONFIG_FILE.exists():
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        return TeamsChannelsConfig(teams=[])
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            return TeamsChannelsConfig(**data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load config: {str(e)}")

def save_config(config: TeamsChannelsConfig):
    """Save configuration to file."""
    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config.model_dump(), f, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save config: {str(e)}")

@router.get("/", response_model=TeamsChannelsConfig)
async def get_config():
    """Get current Teams and Channels configuration."""
    return load_config()

@router.post("/", response_model=TeamsChannelsConfig)
async def update_config(config: TeamsChannelsConfig):
    """Update complete Teams and Channels configuration."""
    save_config(config)
    return config

@router.post("/teams", response_model=TeamConfig)
async def add_team(team: TeamConfig):
    """Add a new team to configuration."""
    config = load_config()
    
    # Check if team already exists
    for existing_team in config.teams:
        if existing_team.team_id == team.team_id:
            raise HTTPException(status_code=400, detail="Team already exists")
    
    config.teams.append(team)
    save_config(config)
    return team

@router.put("/teams/{team_id}", response_model=TeamConfig)
async def update_team(team_id: str, team: TeamConfig):
    """Update an existing team configuration."""
    config = load_config()
    
    for i, existing_team in enumerate(config.teams):
        if existing_team.team_id == team_id:
            config.teams[i] = team
            save_config(config)
            return team
    
    raise HTTPException(status_code=404, detail="Team not found")

@router.delete("/teams/{team_id}")
async def delete_team(team_id: str):
    """Delete a team from configuration."""
    config = load_config()
    
    for i, team in enumerate(config.teams):
        if team.team_id == team_id:
            config.teams.pop(i)
            save_config(config)
            return {"message": "Team deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Team not found")

@router.post("/teams/{team_id}/channels", response_model=ChannelConfig)
async def add_channel(team_id: str, channel: ChannelConfig):
    """Add a channel to a team."""
    config = load_config()
    
    for team in config.teams:
        if team.team_id == team_id:
            # Check if channel already exists
            for existing_channel in team.channels:
                if existing_channel.channel_id == channel.channel_id:
                    raise HTTPException(status_code=400, detail="Channel already exists")
            
            team.channels.append(channel)
            save_config(config)
            return channel
    
    raise HTTPException(status_code=404, detail="Team not found")

@router.delete("/teams/{team_id}/channels/{channel_id}")
async def delete_channel(team_id: str, channel_id: str):
    """Delete a channel from a team."""
    config = load_config()
    
    for team in config.teams:
        if team.team_id == team_id:
            for i, channel in enumerate(team.channels):
                if channel.channel_id == channel_id:
                    team.channels.pop(i)
                    save_config(config)
                    return {"message": "Channel deleted successfully"}
            raise HTTPException(status_code=404, detail="Channel not found")
    
    raise HTTPException(status_code=404, detail="Team not found")
