#!/bin/bash

set -e

echo "Starting build process..."

# Create directories
mkdir -p /opt/render/project/src/.render

# Download Chrome
CHROME_URL="https://dl.google.com/linux/direct/google-chrome-stable_current_x64.deb"
CHROME_DOWNLOAD_DIR="/tmp/chrome"
mkdir -p "$CHROME_DOWNLOAD_DIR"

echo "Downloading Chrome..."
wget -q -O "$CHROME_DOWNLOAD_DIR/chrome.deb" "$CHROME_URL"

# Extract Chrome from .deb package
cd "$CHROME_DOWNLOAD_DIR"
ar x chrome.deb
tar -xf data.tar.xz

# Find Chrome binary
CHROME_BINARY=$(find . -name "google-chrome" | head -n 1)
if [ -z "$CHROME_BINARY" ]; then
    echo "Error: Chrome binary not found"
    exit 1
fi

# Copy Chrome to render directory
cp "$CHROME_BINARY" /opt/render/project/src/.render/chrome
chmod +x /opt/render/project/src/.render/chrome

# Print Chrome version
/opt/render/project/src/.render/chrome --version

# Download matching ChromeDriver
CHROME_VERSION=$(/opt/render/project/src/.render/chrome --version | cut -d' ' -f3 | cut -d'.' -f1)
CHROMEDRIVER_URL=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
CHROMEDRIVER_DOWNLOAD="https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_URL/chromedriver_linux64.zip"

echo "Downloading ChromeDriver version: $CHROMEDRIVER_URL"
wget -q -O "/tmp/chromedriver.zip" "$CHROMEDRIVER_DOWNLOAD"

# Extract ChromeDriver
unzip -o "/tmp/chromedriver.zip" -d /opt/render/project/src/.render/
chmod +x /opt/render/project/src/.render/chromedriver

# Verify ChromeDriver
/opt/render/project/src/.render/chromedriver --version

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "Build process completed successfully"