from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import json
import os

app = FastAPI(title="Intercom-Teams Config API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConfigSettings(BaseModel):
    azure_client_id: Optional[str] = None
    azure_tenant_id: Optional[str] = None
    intercom_access_token: Optional[str] = None
    default_team_id: Optional[str] = None
    default_channel_name: Optional[str] = None

CONFIG_FILE = ".env"

@app.get("/")
async def root():
    return {"status": "ok", "message": "Config API running"}

@app.get("/api/config")
async def get_config():
    """Get current configuration (without secrets)"""
    try:
        config = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        # Mask secrets
                        if 'SECRET' in key or 'TOKEN' in key:
                            config[key] = '***' if value else ''
                        else:
                            config[key] = value
        return {"config": config}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/config")
async def update_config(settings: ConfigSettings):
    """Update configuration settings"""
    try:
        config_dict = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        config_dict[key] = value
        
        # Update with new values
        if settings.azure_client_id:
            config_dict['AZURE_CLIENT_ID'] = settings.azure_client_id
        if settings.azure_tenant_id:
            config_dict['AZURE_TENANT_ID'] = settings.azure_tenant_id
        if settings.intercom_access_token:
            config_dict['INTERCOM_ACCESS_TOKEN'] = settings.intercom_access_token
        if settings.default_team_id:
            config_dict['DEFAULT_TEAM_ID'] = settings.default_team_id
        if settings.default_channel_name:
            config_dict['DEFAULT_CHANNEL_NAME'] = settings.default_channel_name
        
        # Write back to file
        with open(CONFIG_FILE, 'w') as f:
            for key, value in config_dict.items():
                f.write(f"{key}={value}\n")
        
        return {"status": "success", "message": "Configuration updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
