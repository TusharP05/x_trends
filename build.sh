#!/bin/bash

set -e
set -x

# Comprehensive logging
exec > >(tee /tmp/chrome_install_log.txt) 2>&1

echo "===== Chrome Installation Debug Script ====="

# Create directories with full path
mkdir -p /opt/render/project/src/.render/chrome
mkdir -p /tmp/chrome-install

# Download Chrome
CHROME_URL="https://dl.google.com/linux/direct/google-chrome-stable_current_x64.deb"
CHROME_DOWNLOAD_PATH="/tmp/chrome-install/chrome.deb"

# Download Chrome package
wget -O "$CHROME_DOWNLOAD_PATH" "$CHROME_URL"

# Extract Chrome
cd /tmp/chrome-install
ar x chrome.deb
tar -xf data.tar.xz

# Find and copy Chrome binary
CHROME_BINARY=$(find . -name "google-chrome" | head -n 1)
if [ -z "$CHROME_BINARY" ]; then
    echo "CRITICAL: No Chrome binary found in extracted files"
    exit 1
fi

# Copy Chrome binary with verbose output
echo "Copying Chrome binary..."
cp "$CHROME_BINARY" /opt/render/project/src/.render/chrome/google-chrome
chmod +x /opt/render/project/src/.render/chrome/google-chrome

# Symlink to standard locations
mkdir -p /opt/google/chrome
ln -sf /opt/render/project/src/.render/chrome/google-chrome /opt/google/chrome/google-chrome
ln -sf /opt/render/project/src/.render/chrome/google-chrome /usr/bin/google-chrome

# Download matching ChromeDriver
CHROME_VERSION=$(/opt/render/project/src/.render/chrome/google-chrome --version | cut -d' ' -f3 | cut -d'.' -f1)
CHROMEDRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
CHROMEDRIVER_DOWNLOAD="https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"

echo "Downloading ChromeDriver version: $CHROMEDRIVER_VERSION"
wget -O "/tmp/chromedriver.zip" "$CHROMEDRIVER_DOWNLOAD"

# Extract ChromeDriver
unzip -o "/tmp/chromedriver.zip" -d /opt/render/project/src/.render/
chmod +x /opt/render/project/src/.render/chromedriver

# Verification steps
echo "===== Installation Verification ====="
echo "Chrome binary location:"
ls -l /opt/render/project/src/.render/chrome/google-chrome
/opt/render/project/src/.render/chrome/google-chrome --version

echo "ChromeDriver location:"
ls -l /opt/render/project/src/.render/chromedriver
/opt/render/project/src/.render/chromedriver --version

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "===== Build Process Completed Successfully ====="

# Print out all relevant paths for debugging
echo "===== PATH Information ====="
echo "Current PATH: $PATH"
echo "Which google-chrome: $(which google-chrome)"
echo "Chrome binary full path: $(readlink -f /opt/render/project/src/.render/chrome/google-chrome)"