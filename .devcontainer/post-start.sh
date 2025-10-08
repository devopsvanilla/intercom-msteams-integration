#!/bin/bash

# Teams-Intercom Integration - Post Start Script
# This script runs every time the container starts

set -e

echo "🌅 Running post-start setup..."

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Check if required environment variables are set
echo "🔍 Checking environment configuration..."

ENV_FILE=".env"
if [ ! -f "$ENV_FILE" ]; then
    echo "⚠️  Warning: .env file not found. Copying from .env.example"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "📝 Please edit .env file with your actual credentials"
    fi
fi

# Check if GitHub CLI is authenticated
if command -v gh &> /dev/null; then
    if ! gh auth status &> /dev/null; then
        echo "🔑 GitHub CLI not authenticated. Run 'gh auth login' to authenticate."
    else
        echo "✅ GitHub CLI is authenticated"
    fi
fi

# Update Git configuration if needed
if [ -n "$GIT_USER_NAME" ] && [ -n "$GIT_USER_EMAIL" ]; then
    git config --global user.name "$GIT_USER_NAME"
    git config --global user.email "$GIT_USER_EMAIL"
    echo "✅ Git configuration updated"
fi

# Check if dependencies are installed
if [ -f "requirements.txt" ]; then
    echo "📦 Checking Python dependencies..."
    pip list --quiet > /tmp/installed_packages.txt

    # Check if key packages are installed
    if ! grep -q "fastapi" /tmp/installed_packages.txt; then
        echo "⚠️  Some dependencies might be missing. Run 'make install' to install them."
    else
        echo "✅ Python dependencies look good"
    fi
fi

# Display helpful information
echo ""
echo "🚀 Development environment is ready!"
echo ""
echo "📊 Quick status:"
echo "  • Python: $(python --version)"
echo "  • Pip: $(pip --version | cut -d' ' -f1-2)"
echo "  • Git: $(git --version)"
echo "  • GitHub CLI: $(gh --version | head -n1)"
echo ""
echo "🔧 Available commands:"
echo "  • make dev      - Start development server"
echo "  • make test     - Run tests"
echo "  • make lint     - Run code linting"
echo "  • make format   - Format code"
echo "  • make help     - Show all commands"
echo ""
echo "📝 Next steps:"
echo "  1. Edit .env file with your credentials"
echo "  2. Run 'make install' to install dependencies"
echo "  3. Run 'make dev' to start the development server"
echo ""

# Start services if requested
if [ "$AUTO_START_SERVICES" = "true" ]; then
    echo "🔄 Auto-starting development server..."
    make dev &
fi

echo "Happy coding! 🎉"
