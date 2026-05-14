#!/bin/bash

set -e

echo "Installing testing tools..."
pip install pytest pytest-asyncio requests playwright respx pytest-playwright
playwright install chromium

echo "Testing tools installation complete."
