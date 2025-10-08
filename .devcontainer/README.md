# Teams-Intercom Integration Development Container

This development container provides a complete Python development environment for the Teams-Intercom Integration project.

## Quick Start

After the container is created, follow these steps:

### 1. Install Dependencies

```bash
# Option 1: Use the convenience script
./install_deps.sh

# Option 2: Use make
make install

# Option 3: Manual installation
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 2. (Optional) Set up Virtual Environment

If you prefer to use a virtual environment within the container:

```bash
# Use the convenience script
./setup_venv.sh

# Or manually
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy and edit environment file
cp .env.example .env
# Edit .env with your actual credentials
```

### 4. Start Development

```bash
# Run development server
make dev

# Or manually
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Available Commands

The container includes several helpful commands via the Makefile:

```bash
make help          # Show all available commands
make install       # Install dependencies
make install-dev   # Install in development mode
make setup-venv    # Create virtual environment
make test          # Run tests
make lint          # Run linting
make format        # Format code
make typecheck     # Run type checking
make security      # Run security checks
make clean         # Clean cache files
make run           # Run production server
make dev           # Run development server
make reinstall     # Clean and reinstall dependencies
```

## Troubleshooting

### Dependency Installation Issues

If you encounter dependency conflicts:

1. **Clear pip cache:**
   ```bash
   pip cache purge
   ```

2. **Clean and reinstall:**
   ```bash
   make clean
   make reinstall
   ```

3. **Check Python version:**
   ```bash
   python --version  # Should be Python 3.11
   ```

4. **Update pip:**
   ```bash
   pip install --upgrade pip setuptools wheel
   ```

### Virtual Environment Issues

If virtual environment activation fails:

```bash
# Remove existing virtual environment
rm -rf .venv

# Create new one
./setup_venv.sh
```

### Container Permission Issues

If you encounter permission issues:

```bash
# Fix ownership (run as root if needed)
sudo chown -R vscode:vscode /workspaces/intercom-msteams-integration
```

## Development Tools

The container includes:

- **Python 3.11** with pip, setuptools, wheel
- **Code Quality:** black, isort, flake8, pylint, mypy, ruff
- **Testing:** pytest, pytest-asyncio, pytest-cov
- **Security:** bandit, safety
- **Git Tools:** git, GitHub CLI (gh)
- **Development:** pre-commit hooks, VS Code extensions
- **Utilities:** curl, wget, jq, tree, htop

## VS Code Integration

The container automatically configures:

- Python interpreter settings
- Linting and formatting on save
- Debug configurations
- Task runners
- Extension recommendations

## Environment Variables

Required environment variables (set in `.env`):

```env
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_TENANT_ID=your-tenant-id
INTERCOM_ACCESS_TOKEN=your-access-token
INTERCOM_WEBHOOK_SECRET=your-webhook-secret
DEFAULT_TEAM_ID=your-team-id
DEBUG=true
```

## Port Forwarding

The container automatically forwards these ports:

- **8000**: FastAPI Application (main)
- **8080**: Alternative Web Server
- **3000**: Frontend Development
- **5000**: Flask/Debug Server

## Support

For issues with the development container:

1. Check the container logs
2. Rebuild the container: `Ctrl+Shift+P` → "Dev Containers: Rebuild Container"
3. Check the troubleshooting section above
4. Consult the project documentation

## Container Features

This container includes these dev container features:

- **GitHub CLI**: Pre-configured for GitHub integration
- **Docker-in-Docker**: For container development within the container
- **Git**: Latest version for version control
- **Common Utils**: ZSH, Oh My ZSH, and useful utilities

Happy coding! 🚀
