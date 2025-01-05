#!/bin/bash

echo "Starting Chrome installation..."

# Add Google Chrome repository
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list

# Update packages and install Chrome
apt-get update
apt-get install -y google-chrome-stable

# Print Chrome path and version
which google-chrome-stable
google-chrome-stable --version

# Install ChromeDriver
CHROME_VERSION=$(google-chrome-stable --version | cut -d' ' -f3 | cut -d'.' -f1)
CHROMEDRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
echo "Installing ChromeDriver version: $CHROMEDRIVER_VERSION"

wget -q "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
rm chromedriver_linux64.zip

# Create directory if it doesn't exist
mkdir -p /opt/render/project/src/.render/

# Create symlinks
ln -sf $(which google-chrome-stable) /opt/render/project/src/.render/chrome
ln -sf /usr/local/bin/chromedriver /opt/render/project/src/.render/chromedriver

echo "Chrome installation completed. Installed at: $(which google-chrome-stable)"

# Install Python dependencies
pip install -r requirements.txt