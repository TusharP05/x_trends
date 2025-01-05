#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting Chrome and dependencies installation..."

# Ensure apt is up to date
apt-get update

# Install necessary dependencies
apt-get install -y \
    wget \
    unzip \
    gnupg \
    curl \
    software-properties-common

# Add Google Chrome repository
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list

# Update packages again
apt-get update

# Install Chrome
apt-get install -y google-chrome-stable

# Verify Chrome installation
CHROME_PATH=$(which google-chrome-stable)
if [ -z "$CHROME_PATH" ]; then
    echo "Error: Google Chrome not found after installation"
    exit 1
fi

echo "Chrome installed at: $CHROME_PATH"
$CHROME_PATH --version

# Install ChromeDriver
CHROME_VERSION=$(google-chrome-stable --version | cut -d' ' -f3 | cut -d'.' -f1)
CHROMEDRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
echo "Installing ChromeDriver version: $CHROMEDRIVER_VERSION"

wget -q "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip -o chromedriver_linux64.zip
chmod +x chromedriver
mv chromedriver /usr/local/bin/chromedriver

# Create directories
mkdir -p /opt/render/project/src/.render/

# Create symlinks
ln -sf "$CHROME_PATH" /opt/render/project/src/.render/chrome
ln -sf /usr/local/bin/chromedriver /opt/render/project/src/.render/chromedriver

# Verify ChromeDriver
CHROMEDRIVER_PATH=$(which chromedriver)
if [ -z "$CHROMEDRIVER_PATH" ]; then
    echo "Error: ChromeDriver not found after installation"
    exit 1
fi

echo "ChromeDriver installed at: $CHROMEDRIVER_PATH"
chromedriver --version

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "Build script completed successfully"