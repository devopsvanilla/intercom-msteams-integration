#!/bin/bash
echo "📚 Installing project dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "✅ Dependencies installed successfully!"
