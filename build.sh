#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Playwright browsers and dependencies..."
# Install playwright browser (chromium only to save space)
playwright install chromium
# Install system dependencies required by Playwright on Linux
playwright install-deps chromium
