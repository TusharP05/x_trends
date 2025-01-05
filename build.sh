#!/usr/bin/env bash
set -eo pipefail

echo "Starting build process..."

# Install system dependencies
apt-get update
apt-get install -y wget gnupg2 curl unzip xvfb

# Install Chrome
echo "Installing Chrome..."
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list
apt-get update
apt-get install -y google-chrome-stable
echo "Chrome installed successfully"

# Get Chrome version
CHROME_VERSION=$(google-chrome --version | awk '{ print $3 }' | cut -d. -f1)
echo "Chrome version: $CHROME_VERSION"

# Install matching ChromeDriver
echo "Installing ChromeDriver..."
CHROMEDRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
echo "ChromeDriver version: $CHROMEDRIVER_VERSION"

wget -q "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip -q chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
rm chromedriver_linux64.zip

# Verify installations
echo "Verifying installations..."
google-chrome --version
chromedriver --version

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build process completed!"