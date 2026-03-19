#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Playwright browsers..."
# Install playwright browser (chromium only to save space)
playwright install chromium

# Note: On Render's standard native Python environment, we cannot run `playwright install-deps`
# because it requires sudo/root access (which causes the 'su: Authentication failure').
# Render's native environments usually have the necessary libraries pre-installed.
# If this fails at runtime, we will need to switch to a Docker environment or use Render's build cache.
echo "Build script completed successfully."
