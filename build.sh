#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Playwright browsers..."
# Let Playwright install in its default cache directory where it expects it to be
playwright install chromium

echo "Build script completed successfully."
