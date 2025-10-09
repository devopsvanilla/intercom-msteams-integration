#!/bin/bash

# Teams-Intercom Integration - Post Create Script
# This script runs after the container is created

set -e

echo "🚀 Starting post-create setup for Teams-Intercom Integration..."

# Update package lists
echo "📦 Updating package lists..."
sudo apt-get update

# Install additional system packages
echo "🔧 Installing additional system packages..."
sudo apt-get install -y \
    curl \
    wget \
    unzip \
    jq \
    tree \
    htop \
    vim \
    nano \
    sqlite3 \
    postgresql-client \
    redis-tools \
    netcat \
    telnet \
    iputils-ping \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev

# Install Python development tools
echo "🐍 Installing Python development tools..."
pip install --upgrade pip setuptools wheel

# Install project dependencies (with error handling)
echo "📚 Setting up dependency installation (manual step required)..."
if [ -f "requirements.txt" ]; then
    echo "ℹ️  Dependencies can be installed later with: pip install -r requirements.txt"
    echo "ℹ️  Or use: make install"
    # Create a convenience script for dependency installation
    cat > install_deps.sh << 'EOF'
#!/bin/bash
echo "📚 Installing project dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "✅ Dependencies installed successfully!"
EOF
    chmod +x install_deps.sh
else
    echo "⚠️  No requirements.txt found"
fi

# Install development dependencies
echo "🛠️ Installing development dependencies..."
pip install \
    black \
    isort \
    flake8 \
    pylint \
    mypy \
    pytest \
    pytest-asyncio \
    pytest-cov \
    pytest-mock \
    bandit \
    safety \
    pre-commit \
    jupyterlab \
    ipython \
    python-dotenv \
    httpx

# Install Ruff (fast Python linter and formatter)
echo "⚡ Installing Ruff..."
pip install ruff

# Setup pre-commit hooks
echo "🪝 Setting up pre-commit hooks..."
if [ -f ".pre-commit-config.yaml" ]; then
    pre-commit install
    pre-commit install --hook-type commit-msg
fi

# Configure Git (if not already configured)
echo "📝 Configuring Git..."
if [ -z "$(git config --global user.name)" ]; then
    git config --global user.name "DevOps Vanilla"
fi

if [ -z "$(git config --global user.email)" ]; then
    git config --global user.email "devops@vanilla.com"
fi

# Set Git to use main as default branch
git config --global init.defaultBranch main

# Configure GitHub CLI if token is available
if [ -n "$GITHUB_TOKEN" ]; then
    echo "🔑 Configuring GitHub CLI..."
    echo "$GITHUB_TOKEN" | gh auth login --with-token
fi

# Create useful directories
echo "📁 Creating project directories..."
mkdir -p \
    .vscode \
    logs \
    tests \
    docs \
    scripts \
    data

# Create virtual environment setup script (for manual execution)
echo "🌍 Creating virtual environment setup script..."
cat > setup_venv.sh << 'EOF'
#!/bin/bash
echo "🌍 Setting up Python virtual environment..."
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel

if [ -f "requirements.txt" ]; then
    echo "📚 Installing dependencies..."
    pip install -r requirements.txt
fi

echo "✅ Virtual environment setup complete!"
echo "💡 To activate: source .venv/bin/activate"
EOF
chmod +x setup_venv.sh

echo "ℹ️  Virtual environment can be created later with: ./setup_venv.sh"

# Install project in development mode
if [ -f "setup.py" ]; then
    pip install -e .
fi

# Create useful aliases
echo "🔗 Setting up aliases..."
cat >> ~/.bashrc << 'EOF'

# Project aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# Python aliases
alias py='python'
alias pip='python -m pip'
alias pytest='python -m pytest'
alias black='python -m black'
alias isort='python -m isort'
alias flake8='python -m flake8'
alias mypy='python -m mypy'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git pull'
alias gd='git diff'
alias gb='git branch'
alias gco='git checkout'

# Project specific aliases
alias rundev='uvicorn main:app --reload --host 0.0.0.0 --port 8000'
alias runprod='python main.py'
alias test='pytest -v'
alias lint='flake8 . && pylint *.py'
alias format='black . && isort .'
alias typecheck='mypy .'
alias security='bandit -r . && safety check'

# Docker aliases
alias d='docker'
alias dc='docker-compose'
alias dps='docker ps'
alias di='docker images'

# Utility aliases
alias reload='source ~/.bashrc'
alias h='history'
alias c='clear'
alias path='echo -e ${PATH//:/\\n}'
alias ports='netstat -tuln'
EOF

# Setup ZSH configuration (if using oh-my-zsh)
if [ -d "$HOME/.oh-my-zsh" ]; then
    echo "🐚 Configuring ZSH..."
    cat >> ~/.zshrc << 'EOF'

# Project aliases (same as bash)
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'

# Python aliases
alias py='python'
alias pip='python -m pip'
alias pytest='python -m pytest'
alias black='python -m black'
alias isort='python -m isort'
alias flake8='python -m flake8'
alias mypy='python -m mypy'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git pull'
alias gd='git diff'
alias gb='git branch'
alias gco='git checkout'

# Project specific aliases
alias rundev='uvicorn main:app --reload --host 0.0.0.0 --port 8000'
alias runprod='python main.py'
alias test='pytest -v'
alias lint='flake8 . && pylint *.py'
alias format='black . && isort .'
alias typecheck='mypy .'
alias security='bandit -r . && safety check'

# Enable auto-activation of virtual environment
if [[ -f ".venv/bin/activate" ]]; then
    source .venv/bin/activate
fi
EOF
fi

# Create VS Code settings if they don't exist
echo "⚙️ Creating VS Code workspace settings..."
mkdir -p .vscode

cat > .vscode/settings.json << 'EOF'
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.path": "./.venv/bin/isort",
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/.pytest_cache": true,
        "**/.mypy_cache": true,
        "**/.coverage": true,
        "**/htmlcov": true,
        "**/.venv": false
    }
}
EOF

# Create launch configuration for debugging
cat > .vscode/launch.json << 'EOF'
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            },
            "args": []
        },
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "Python: Pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "-v",
                "${workspaceFolder}/tests"
            ],
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
EOF

# Create tasks.json for common tasks
cat > .vscode/tasks.json << 'EOF'
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Install Dependencies",
            "type": "shell",
            "command": "pip",
            "args": ["install", "-r", "requirements.txt"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Run Tests",
            "type": "shell",
            "command": "pytest",
            "args": ["-v"],
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Format Code",
            "type": "shell",
            "command": "black",
            "args": ["."],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Sort Imports",
            "type": "shell",
            "command": "isort",
            "args": ["."],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Lint Code",
            "type": "shell",
            "command": "flake8",
            "args": ["."],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Type Check",
            "type": "shell",
            "command": "mypy",
            "args": ["."],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "panel": "new"
            }
        },
        {
            "label": "Run FastAPI Dev",
            "type": "shell",
            "command": "uvicorn",
            "args": ["main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "panel": "new"
            },
            "isBackground": true
        }
    ]
}
EOF

# Create initial test environment file
echo "🔐 Creating test environment file..."
if [ ! -f ".env.test" ]; then
    cat > .env.test << 'EOF'
# Test Environment Variables
AZURE_CLIENT_ID=test-client-id
AZURE_CLIENT_SECRET=test-client-secret
AZURE_TENANT_ID=test-tenant-id
INTERCOM_ACCESS_TOKEN=test-access-token
INTERCOM_WEBHOOK_SECRET=test-webhook-secret
DEFAULT_TEAM_ID=test-team-id
DEBUG=true
EOF
fi

# Create pre-commit configuration
echo "🔍 Creating pre-commit configuration..."
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      - id: check-xml
      - id: debug-statements
      - id: check-docstring-first
      - id: check-merge-conflict
      - id: check-executables-have-shebangs

  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203,W503]

  - repo: https://github.com/pycqa/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-r', '.']
        exclude: ^tests/

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.280
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
EOF

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pre-commit install

# Create a simple Makefile for common tasks
echo "📝 Creating Makefile..."
cat > Makefile << 'EOF'
.PHONY: help install test lint format clean run dev security

help:
	@echo "Available commands:"
	@echo "  install     Install dependencies"
	@echo "  test        Run tests"
	@echo "  lint        Run linting"
	@echo "  format      Format code"
	@echo "  typecheck   Run type checking"
	@echo "  security    Run security checks"
	@echo "  clean       Clean cache files"
	@echo "  run         Run production server"
	@echo "  dev         Run development server"

install:
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt

install-dev: install
	pip install -e .

setup-venv:
	python -m venv .venv
	@echo "Virtual environment created. Activate with: source .venv/bin/activate"

clean-deps:
	pip freeze | grep -v "^-e" | xargs pip uninstall -y

reinstall: clean-deps install

test:
	pytest -v --cov=. --cov-report=html

lint:
	flake8 .
	pylint *.py

format:
	black .
	isort .

typecheck:
	mypy .

security:
	bandit -r .
	safety check

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -f .coverage

run:
	python main.py

dev:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000
EOF

# Create gitignore additions for Python development
echo "📄 Updating .gitignore..."
cat >> .gitignore << 'EOF'

# Python Development
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
.venv/
venv/
ENV/
env/

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/
coverage.xml
*.cover
*.py,cover
.hypothesis/

# Type Checking
.mypy_cache/
.dmypy.json
dmypy.json

# IDEs
.vscode/settings.json
.idea/
*.swp
*.swo
*~

# Environment files
.env
.env.local
.env.development
.env.production

# Logs
logs/
*.log

# Database
*.db
*.sqlite3

# Cache
.cache/
.ruff_cache/

# OS
.DS_Store
Thumbs.db
EOF

echo "✅ Post-create setup completed successfully!"
echo ""
echo "🎉 Your Teams-Intercom Integration development environment is ready!"
echo ""

# Executar verificação de configurações herdadas
echo "🔍 Verificando configurações herdadas do host..."
bash .devcontainer/check-config.sh

echo "Available commands:"
echo "  - make help    : Show all available commands"
echo "  - make dev     : Run development server"
echo "  - make test    : Run tests"
echo "  - make lint    : Run linting"
echo "  - make format  : Format code"
echo ""
echo "Happy coding! 🚀"
