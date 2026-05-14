#!/bin/bash

set -e

echo "Installing Backend dependencies..."
# Use a virtual environment if possible, but for simplicity in this script:
pip install fastapi uvicorn pydantic python-dotenv httpx respx pytest-playwright

echo "Installing Frontend dependencies..."
# This assumes node and npm are installed
cd src/frontend
npm install --no-audit --no-fund
cd ../..

echo "Installation complete."
