import React from 'react';
import TeamChannelsConfig from './TeamChannelsConfig';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Intercom-MS Teams Integration</h1>
        <p>Manage Teams and Channels Configuration</p>
      </header>
      <main className="App-main">
        <TeamChannelsConfig />
      </main>
      <footer className="App-footer">
        <p>&copy; 2025 DevOps Vanilla - Intercom & MS Teams Integration</p>
      </footer>
    </div>
  );
}

export default App;
