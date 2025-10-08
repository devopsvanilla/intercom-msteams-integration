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
