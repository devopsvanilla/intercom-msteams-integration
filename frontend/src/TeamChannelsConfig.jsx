import React, { useState, useEffect } from 'react';
import './TeamChannelsConfig.css';

const TeamChannelsConfig = () => {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingTeam, setEditingTeam] = useState(null);
  const [newTeam, setNewTeam] = useState({ team_id: '', team_name: '', channels: [] });
  const [newChannel, setNewChannel] = useState({ channel_id: '', channel_name: '' });
  const [showAddTeam, setShowAddTeam] = useState(false);

  const API_BASE_URL = '/api/config';

  useEffect(() => {
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    try {
      setLoading(true);
      const response = await fetch(API_BASE_URL);
      if (!response.ok) throw new Error('Failed to fetch configuration');
      const data = await response.json();
      setTeams(data.teams || []);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const saveConfig = async (updatedTeams) => {
    try {
      const response = await fetch(API_BASE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ teams: updatedTeams })
      });
      if (!response.ok) throw new Error('Failed to save configuration');
      const data = await response.json();
      setTeams(data.teams || []);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleAddTeam = async () => {
    if (!newTeam.team_id || !newTeam.team_name) {
      setError('Team ID and Name are required');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/teams`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTeam)
      });
      if (!response.ok) throw new Error('Failed to add team');
      await fetchConfig();
      setNewTeam({ team_id: '', team_name: '', channels: [] });
      setShowAddTeam(false);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteTeam = async (teamId) => {
    if (!window.confirm('Are you sure you want to delete this team?')) return;

    try {
      const response = await fetch(`${API_BASE_URL}/teams/${teamId}`, {
        method: 'DELETE'
      });
      if (!response.ok) throw new Error('Failed to delete team');
      await fetchConfig();
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleAddChannel = async (teamId) => {
    if (!newChannel.channel_id || !newChannel.channel_name) {
      setError('Channel ID and Name are required');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/teams/${teamId}/channels`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newChannel)
      });
      if (!response.ok) throw new Error('Failed to add channel');
      await fetchConfig();
      setNewChannel({ channel_id: '', channel_name: '' });
      setEditingTeam(null);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteChannel = async (teamId, channelId) => {
    if (!window.confirm('Are you sure you want to delete this channel?')) return;

    try {
      const response = await fetch(`${API_BASE_URL}/teams/${teamId}/channels/${channelId}`, {
        method: 'DELETE'
      });
      if (!response.ok) throw new Error('Failed to delete channel');
      await fetchConfig();
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <div className="loading">Loading configuration...</div>;

  return (
    <div className="teams-channels-config">
      <h1>Teams & Channels Configuration</h1>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

      <div className="config-header">
        <button
          className="btn-primary"
          onClick={() => setShowAddTeam(!showAddTeam)}
        >
          {showAddTeam ? 'Cancel' : '+ Add Team'}
        </button>
        <button className="btn-secondary" onClick={fetchConfig}>
          🔄 Refresh
        </button>
      </div>

      {showAddTeam && (
        <div className="add-team-form">
          <h3>Add New Team</h3>
          <input
            type="text"
            placeholder="Team ID"
            value={newTeam.team_id}
            onChange={(e) => setNewTeam({ ...newTeam, team_id: e.target.value })}
          />
          <input
            type="text"
            placeholder="Team Name"
            value={newTeam.team_name}
            onChange={(e) => setNewTeam({ ...newTeam, team_name: e.target.value })}
          />
          <button className="btn-success" onClick={handleAddTeam}>
            Save Team
          </button>
        </div>
      )}

      <div className="teams-list">
        {teams.length === 0 ? (
          <div className="empty-state">
            <p>No teams configured yet. Click "Add Team" to get started.</p>
          </div>
        ) : (
          teams.map((team) => (
            <div key={team.team_id} className="team-card">
              <div className="team-header">
                <div className="team-info">
                  <h2>{team.team_name}</h2>
                  <span className="team-id">ID: {team.team_id}</span>
                </div>
                <div className="team-actions">
                  <button
                    className="btn-edit"
                    onClick={() => setEditingTeam(editingTeam === team.team_id ? null : team.team_id)}
                  >
                    {editingTeam === team.team_id ? 'Close' : '+ Add Channel'}
                  </button>
                  <button
                    className="btn-danger"
                    onClick={() => handleDeleteTeam(team.team_id)}
                  >
                    Delete Team
                  </button>
                </div>
              </div>

              {editingTeam === team.team_id && (
                <div className="add-channel-form">
                  <h4>Add Channel</h4>
                  <input
                    type="text"
                    placeholder="Channel ID"
                    value={newChannel.channel_id}
                    onChange={(e) => setNewChannel({ ...newChannel, channel_id: e.target.value })}
                  />
                  <input
                    type="text"
                    placeholder="Channel Name"
                    value={newChannel.channel_name}
                    onChange={(e) => setNewChannel({ ...newChannel, channel_name: e.target.value })}
                  />
                  <button
                    className="btn-success"
                    onClick={() => handleAddChannel(team.team_id)}
                  >
                    Save Channel
                  </button>
                </div>
              )}

              <div className="channels-list">
                <h3>Channels ({team.channels?.length || 0})</h3>
                {team.channels && team.channels.length > 0 ? (
                  <ul>
                    {team.channels.map((channel) => (
                      <li key={channel.channel_id} className="channel-item">
                        <div className="channel-info">
                          <strong>{channel.channel_name}</strong>
                          <span className="channel-id">ID: {channel.channel_id}</span>
                        </div>
                        <button
                          className="btn-danger-sm"
                          onClick={() => handleDeleteChannel(team.team_id, channel.channel_id)}
                        >
                          Delete
                        </button>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="no-channels">No channels configured for this team.</p>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default TeamChannelsConfig;
