#!/usr/bin/env bash
set -euo pipefail

echo "Starting build process..."

# Update package list
apt-get update

# Install dependencies
apt-get install -y wget gnupg2 unzip

# Add Google Chrome repository key
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Add Google Chrome repository
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Update package list again
apt-get update

# Install Google Chrome
apt-get install -y google-chrome-stable

# Verify Chrome installation
echo "Checking Chrome installation..."
which google-chrome-stable
google-chrome-stable --version

# Get Chrome version for matching ChromeDriver
CHROME_VERSION=$(google-chrome-stable --version | cut -d ' ' -f 3 | cut -d '.' -f 1)

# Download and install ChromeDriver
echo "Installing ChromeDriver..."
wget -q "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_VERSION.0.6261.94/linux64/chromedriver-linux64.zip"
unzip chromedriver-linux64.zip
mv chromedriver-linux64/chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

# Verify ChromeDriver installation
echo "Checking ChromeDriver installation..."
which chromedriver
chromedriver --version

# Create symlink to ensure Chrome is found in the expected location
ln -s $(which google-chrome-stable) /usr/bin/google-chrome-stable

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build completed successfully!"