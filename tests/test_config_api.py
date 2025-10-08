"""Tests for Teams and Channels Configuration API."""


import pytest

# Import the FastAPI app (this would need to be integrated into main.py)
# For now, we'll test the individual functions
from api.config_api import (
    ChannelConfig,
    TeamConfig,
    TeamsChannelsConfig,
    load_config,
    save_config,
)


@pytest.fixture
def test_config_file(tmp_path):
    """Create a temporary config file for testing."""
    test_file = tmp_path / "test_config.json"
    # Temporarily replace CONFIG_FILE
    import api.config_api as config_api

    original_config = config_api.CONFIG_FILE
    config_api.CONFIG_FILE = test_file
    yield test_file
    config_api.CONFIG_FILE = original_config
    if test_file.exists():
        test_file.unlink()


def test_channel_config_creation():
    """Test ChannelConfig model."""
    channel = ChannelConfig(
        channel_id="19:abcd1234@thread.tacv2", channel_name="Support"
    )
    assert channel.channel_id == "19:abcd1234@thread.tacv2"
    assert channel.channel_name == "Support"


def test_team_config_creation():
    """Test TeamConfig model."""
    team = TeamConfig(team_id="abc123", team_name="Customer Success", channels=[])
    assert team.team_id == "abc123"
    assert team.team_name == "Customer Success"
    assert len(team.channels) == 0


def test_team_config_with_channels():
    """Test TeamConfig with channels."""
    channel1 = ChannelConfig(channel_id="19:ch1@thread.tacv2", channel_name="General")
    channel2 = ChannelConfig(channel_id="19:ch2@thread.tacv2", channel_name="Support")
    team = TeamConfig(
        team_id="team1", team_name="Sales Team", channels=[channel1, channel2]
    )
    assert len(team.channels) == 2
    assert team.channels[0].channel_name == "General"
    assert team.channels[1].channel_name == "Support"


def test_teams_channels_config_creation():
    """Test TeamsChannelsConfig model."""
    config = TeamsChannelsConfig(teams=[])
    assert len(config.teams) == 0
    assert config.teams == []


def test_load_config_empty(test_config_file):
    """Test loading config when file doesn't exist."""
    config = load_config()
    assert isinstance(config, TeamsChannelsConfig)
    assert len(config.teams) == 0


def test_save_and_load_config(test_config_file):
    """Test saving and loading configuration."""
    # Create test config
    channel = ChannelConfig(
        channel_id="19:test@thread.tacv2", channel_name="Test Channel"
    )
    team = TeamConfig(team_id="test-team", team_name="Test Team", channels=[channel])
    config = TeamsChannelsConfig(teams=[team])

    # Save config
    save_config(config)

    # Load config
    loaded_config = load_config()

    # Verify
    assert len(loaded_config.teams) == 1
    assert loaded_config.teams[0].team_id == "test-team"
    assert loaded_config.teams[0].team_name == "Test Team"
    assert len(loaded_config.teams[0].channels) == 1
    assert loaded_config.teams[0].channels[0].channel_id == "19:test@thread.tacv2"
    assert loaded_config.teams[0].channels[0].channel_name == "Test Channel"


def test_config_serialization():
    """Test configuration serialization."""
    channel = ChannelConfig(channel_id="19:abc@thread.tacv2", channel_name="General")
    team = TeamConfig(team_id="team1", team_name="Engineering", channels=[channel])
    config = TeamsChannelsConfig(teams=[team])

    # Serialize to dict
    config_dict = config.model_dump()

    assert "teams" in config_dict
    assert len(config_dict["teams"]) == 1
    assert config_dict["teams"][0]["team_id"] == "team1"
    assert config_dict["teams"][0]["team_name"] == "Engineering"
    assert len(config_dict["teams"][0]["channels"]) == 1


def test_multiple_teams_config():
    """Test configuration with multiple teams."""
    team1 = TeamConfig(
        team_id="team1",
        team_name="Sales",
        channels=[
            ChannelConfig(channel_id="19:ch1@thread.tacv2", channel_name="General"),
            ChannelConfig(channel_id="19:ch2@thread.tacv2", channel_name="Leads"),
        ],
    )
    team2 = TeamConfig(
        team_id="team2",
        team_name="Support",
        channels=[
            ChannelConfig(channel_id="19:ch3@thread.tacv2", channel_name="Tier 1"),
            ChannelConfig(channel_id="19:ch4@thread.tacv2", channel_name="Tier 2"),
        ],
    )
    config = TeamsChannelsConfig(teams=[team1, team2])

    assert len(config.teams) == 2
    assert config.teams[0].team_name == "Sales"
    assert config.teams[1].team_name == "Support"
    assert len(config.teams[0].channels) == 2
    assert len(config.teams[1].channels) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
