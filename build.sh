#!/usr/bin/env bash
set -e

# Install system dependencies
apt-get update
apt-get install -y wget gnupg2 unzip

# Install Google Chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable

# Print Chrome version
CHROME_VERSION=$(google-chrome --version | cut -d ' ' -f3)
echo "Chrome version: $CHROME_VERSION"

# Install matching ChromeDriver
CHROMEDRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION%%.*}")
echo "Installing ChromeDriver version: $CHROMEDRIVER_VERSION"

wget -q "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
rm chromedriver_linux64.zip

# Print ChromeDriver version
chromedriver --version

# Install Python dependencies
pip install -r requirements.txt