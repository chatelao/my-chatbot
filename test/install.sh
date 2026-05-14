#!/bin/bash

set -e

echo "Installing testing tools..."
pip install pytest pytest-asyncio requests playwright
# playwright install chromium

echo "Testing tools installation complete."
