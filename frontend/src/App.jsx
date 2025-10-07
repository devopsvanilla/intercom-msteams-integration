import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [config, setConfig] = useState({
    azure_client_id: '',
    azure_tenant_id: '',
    intercom_access_token: '',
    default_team_id: '',
    default_channel_name: ''
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  const API_BASE_URL = 'http://localhost:8001';

  useEffect(() => {
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/api/config`);
      const data = await response.json();
      if (data.config) {
        const configObj = {};
        Object.keys(data.config).forEach(key => {
          const lowerKey = key.toLowerCase();
          configObj[lowerKey] = data.config[key];
        });
        setConfig(prev => ({ ...prev, ...configObj }));
      }
    } catch (error) {
      setMessage({ text: 'Error loading configuration', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setConfig(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/api/config`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(config)
      });
      const data = await response.json();
      if (response.ok) {
        setMessage({ text: 'Configuration saved successfully!', type: 'success' });
      } else {
        setMessage({ text: 'Error saving configuration', type: 'error' });
      }
    } catch (error) {
      setMessage({ text: 'Error connecting to API', type: 'error' });
    } finally {
      setLoading(false);
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>Intercom-Teams Integration Config</h1>
        <p className="subtitle">Configure your integration settings</p>
        
        {message.text && (
          <div className={`message ${message.type}`}>
            {message.text}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-section">
            <h2>Azure Configuration</h2>
            <div className="form-group">
              <label htmlFor="azure_client_id">Azure Client ID</label>
              <input
                type="text"
                id="azure_client_id"
                name="azure_client_id"
                value={config.azure_client_id}
                onChange={handleInputChange}
                placeholder="Enter Azure Client ID"
              />
            </div>
            <div className="form-group">
              <label htmlFor="azure_tenant_id">Azure Tenant ID</label>
              <input
                type="text"
                id="azure_tenant_id"
                name="azure_tenant_id"
                value={config.azure_tenant_id}
                onChange={handleInputChange}
                placeholder="Enter Azure Tenant ID"
              />
            </div>
          </div>

          <div className="form-section">
            <h2>Intercom Configuration</h2>
            <div className="form-group">
              <label htmlFor="intercom_access_token">Intercom Access Token</label>
              <input
                type="password"
                id="intercom_access_token"
                name="intercom_access_token"
                value={config.intercom_access_token}
                onChange={handleInputChange}
                placeholder="Enter Intercom Access Token"
              />
            </div>
          </div>

          <div className="form-section">
            <h2>Teams Configuration</h2>
            <div className="form-group">
              <label htmlFor="default_team_id">Default Team ID</label>
              <input
                type="text"
                id="default_team_id"
                name="default_team_id"
                value={config.default_team_id}
                onChange={handleInputChange}
                placeholder="Enter Teams Team ID"
              />
            </div>
            <div className="form-group">
              <label htmlFor="default_channel_name">Default Channel Name</label>
              <input
                type="text"
                id="default_channel_name"
                name="default_channel_name"
                value={config.default_channel_name}
                onChange={handleInputChange}
                placeholder="Enter Channel Name"
              />
            </div>
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Saving...' : 'Save Configuration'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
