#!/bin/bash
set -euo pipefail

echo "Starting build process..."

# Add Google Chrome repository
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'

# Update package lists
apt-get update

# Install required packages
apt-get install -y \
    google-chrome-stable \
    fonts-liberation \
    libgbm1 \
    xvfb \
    unzip \
    wget

# Get the Chrome version
CHROME_VERSION=$(google-chrome --version | cut -d " " -f3 | cut -d"." -f1)
echo "Chrome version: $CHROME_VERSION"

# Download and install the matching ChromeDriver
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
echo "Installing ChromeDriver version: $CHROMEDRIVER_VERSION"

wget -q --continue -P /tmp "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip -o /tmp/chromedriver_linux64.zip -d /tmp/
mv /tmp/chromedriver /usr/local/bin/chromedriver
chown root:root /usr/local/bin/chromedriver
chmod +x /usr/local/bin/chromedriver

# Verify installations
echo "Chrome version installed:"
google-chrome --version
echo "ChromeDriver version installed:"
chromedriver --version

# Install Python requirements
pip install -r requirements.txt

echo "Build completed successfully"