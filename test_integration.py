"""
Testes unitários básicos para a aplicação Teams-Intercom Integration.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from fastapi.testclient import TestClient

from main import app
from graph_client import GraphClient
from intercom_client import IntercomClient
from webhook_handler import WebhookHandler
from config import config


@pytest.fixture
def client():
    """Cliente de teste FastAPI."""
    return TestClient(app)


@pytest.fixture
def mock_graph_client():
    """Mock do cliente Microsoft Graph."""
    client = Mock(spec=GraphClient)
    client._authenticated = True
    client.authenticate = AsyncMock(return_value=True)
    client.get_teams = AsyncMock(return_value=[
        {"id": "team1", "displayName": "Test Team", "description": "Test Description"}
    ])
    client.get_team_channels = AsyncMock(return_value=[
        {"id": "channel1", "displayName": "General", "description": "General channel"}
    ])
    client.send_message = AsyncMock(return_value={
        "id": "msg1", "content": "Test message", "createdDateTime": "2025-01-01T10:00:00Z"
    })
    client.find_or_create_channel = AsyncMock(return_value={
        "id": "channel1", "displayName": "Customer Support"
    })
    return client


@pytest.fixture
def mock_intercom_client():
    """Mock do cliente Intercom."""
    client = Mock(spec=IntercomClient)
    client.get_conversations = AsyncMock(return_value=[
        {"id": "conv1", "source": {"author": {"name": "Test User", "email": "test@example.com"}}}
    ])
    client.get_conversation = AsyncMock(return_value={
        "id": "conv1",
        "source": {"author": {"name": "Test User", "email": "test@example.com"}},
        "conversation_parts": {"conversation_parts": [{"body": "Test message"}]}
    })
    return client


class TestGraphClient:
    """Testes para o cliente Microsoft Graph."""
    
    @pytest.mark.asyncio
    async def test_authentication_success(self):
        """Teste de autenticação bem-sucedida."""
        with patch('graph_client.ClientSecretCredential'), \
             patch('graph_client.GraphServiceClient') as mock_graph:
            
            mock_graph.return_value.me.get = AsyncMock()
            
            client = GraphClient()
            result = await client.authenticate()
            
            assert result is True
            assert client._authenticated is True
    
    @pytest.mark.asyncio
    async def test_authentication_failure(self):
        """Teste de falha na autenticação."""
        with patch('graph_client.ClientSecretCredential'), \
             patch('graph_client.GraphServiceClient') as mock_graph:
            
            mock_graph.return_value.me.get = AsyncMock(side_effect=Exception("Auth failed"))
            
            client = GraphClient()
            result = await client.authenticate()
            
            assert result is False
            assert client._authenticated is False
    
    @pytest.mark.asyncio
    async def test_get_teams_not_authenticated(self):
        """Teste de obter teams sem autenticação."""
        client = GraphClient()
        
        with pytest.raises(Exception, match="Not authenticated"):
            await client.get_teams()
    
    @pytest.mark.asyncio
    async def test_send_message_success(self, mock_graph_client):
        """Teste de envio de mensagem bem-sucedido."""
        with patch('graph_client.ChatMessage'), \
             patch('graph_client.ItemBody'), \
             patch('graph_client.BodyType'):
            
            mock_graph_client.client.teams.by_team_id().channels.by_channel_id().messages.post = AsyncMock(
                return_value=Mock(
                    id="msg1", 
                    body=Mock(content="Test message"),
                    created_date_time=None,
                    from_property=None
                )
            )
            
            client = GraphClient()
            client._authenticated = True
            client.client = mock_graph_client.client
            
            result = await client.send_message("team1", "channel1", "Test message")
            
            assert result["id"] == "msg1"
            assert result["content"] == "Test message"


class TestIntercomClient:
    """Testes para o cliente Intercom."""
    
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Teste do context manager."""
        with patch('intercom_client.aiohttp.ClientSession') as mock_session:
            async with IntercomClient() as client:
                assert client.session is not None
            
            mock_session.return_value.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_conversations_success(self):
        """Teste de obtenção de conversas bem-sucedida."""
        mock_response = Mock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "conversations": [{"id": "conv1", "source": {"author": {"name": "Test"}}}]
        })
        
        with patch('intercom_client.aiohttp.ClientSession') as mock_session:
            mock_session.return_value.request = AsyncMock(return_value=mock_response)
            mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_session.return_value)
            mock_session.return_value.__aexit__ = AsyncMock(return_value=None)
            
            async with IntercomClient() as client:
                conversations = await client.get_conversations()
            
            assert len(conversations) == 1
            assert conversations[0]["id"] == "conv1"
    
    @pytest.mark.asyncio
    async def test_api_error_handling(self):
        """Teste de tratamento de erro da API."""
        mock_response = Mock()
        mock_response.status = 400
        mock_response.json = AsyncMock(return_value={
            "errors": [{"message": "Bad request"}]
        })
        
        with patch('intercom_client.aiohttp.ClientSession') as mock_session:
            mock_session.return_value.request = AsyncMock(return_value=mock_response)
            mock_session.return_value.__aenter__ = AsyncMock(return_value=mock_session.return_value)
            mock_session.return_value.__aexit__ = AsyncMock(return_value=None)
            
            with pytest.raises(Exception, match="Intercom API error"):
                async with IntercomClient() as client:
                    await client.get_conversations()


class TestWebhookHandler:
    """Testes para o handler de webhooks."""
    
    def test_verify_webhook_signature_valid(self):
        """Teste de verificação de assinatura válida."""
        handler = WebhookHandler(Mock(), Mock())
        handler.webhook_secret = "test_secret"
        
        payload = b'{"test": "data"}'
        # Calcular assinatura esperada
        import hmac
        import hashlib
        expected_signature = hmac.new(
            "test_secret".encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        is_valid = handler.verify_webhook_signature(payload, f"sha256={expected_signature}")
        assert is_valid is True
    
    def test_verify_webhook_signature_invalid(self):
        """Teste de verificação de assinatura inválida."""
        handler = WebhookHandler(Mock(), Mock())
        handler.webhook_secret = "test_secret"
        
        payload = b'{"test": "data"}'
        invalid_signature = "invalid_signature"
        
        is_valid = handler.verify_webhook_signature(payload, f"sha256={invalid_signature}")
        assert is_valid is False
    
    @pytest.mark.asyncio
    async def test_process_webhook_conversation_created(self, mock_graph_client, mock_intercom_client):
        """Teste de processamento de webhook de conversa criada."""
        handler = WebhookHandler(mock_graph_client, mock_intercom_client)
        
        with patch.object(handler, '_handle_conversation_created', return_value={"status": "success"}):
            result = await handler.process_webhook(
                "conversation.user.created",
                {"data": {"item": {"id": "conv1"}}}
            )
            
            assert result["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_process_webhook_unknown_event(self, mock_graph_client, mock_intercom_client):
        """Teste de processamento de evento desconhecido."""
        handler = WebhookHandler(mock_graph_client, mock_intercom_client)
        
        result = await handler.process_webhook(
            "unknown.event",
            {"data": {"item": {"id": "conv1"}}}
        )
        
        assert result["status"] == "ignored"
        assert result["event_type"] == "unknown.event"


class TestMainApp:
    """Testes para a aplicação principal."""
    
    def test_health_check(self, client):
        """Teste do endpoint de health check."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_webhook_endpoint_missing_signature(self, client):
        """Teste do endpoint webhook sem assinatura."""
        with patch('main.webhook_handler') as mock_handler:
            mock_handler.verify_webhook_signature.return_value = False
            
            response = client.post("/webhooks/intercom", json={"topic": "test"})
            assert response.status_code == 401
    
    def test_webhook_endpoint_invalid_json(self, client):
        """Teste do endpoint webhook com JSON inválido."""
        with patch('main.webhook_handler') as mock_handler:
            mock_handler.verify_webhook_signature.return_value = True
            
            response = client.post(
                "/webhooks/intercom", 
                data="invalid json",
                headers={"Content-Type": "application/json"}
            )
            assert response.status_code == 400
    
    def test_webhook_endpoint_missing_topic(self, client):
        """Teste do endpoint webhook sem tópico."""
        with patch('main.webhook_handler') as mock_handler:
            mock_handler.verify_webhook_signature.return_value = True
            
            response = client.post("/webhooks/intercom", json={"data": "test"})
            assert response.status_code == 400


class TestConfig:
    """Testes para configuração."""
    
    def test_config_loading(self):
        """Teste de carregamento da configuração."""
        assert config.host == "0.0.0.0"
        assert config.port == 8000
        assert config.webhook_path == "/webhooks/intercom"
        assert config.default_channel_name == "Customer Support"
    
    def test_azure_config(self):
        """Teste da configuração Azure."""
        assert "User.Read" in config.azure.scopes
        assert "Team.ReadWrite.All" in config.azure.scopes
        assert "Channel.ReadWrite.All" in config.azure.scopes


if __name__ == "__main__":
    pytest.main([__file__])