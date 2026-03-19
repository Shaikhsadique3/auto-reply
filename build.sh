#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Playwright browsers..."
# Store playwright browsers in a cacheable path
export PLAYWRIGHT_BROWSERS_PATH=/opt/render/project/playwright
playwright install chromium

echo "Build script completed successfully."
