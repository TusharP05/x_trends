#!/usr/bin/env bash

set -o errexit

STORAGE_DIR=/opt/render/project/.render
CHROMEDRIVER_DIR="$STORAGE_DIR/chromedriver"

if [[ ! -d $STORAGE_DIR/chrome ]]; then
   echo "...Downloading Chrome"
   mkdir -p $STORAGE_DIR/chrome
   cd $STORAGE_DIR/chrome
   wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
   rm ./google-chrome-stable_current_amd64.deb
else
   echo "...Using Chrome from cache"
fi

# Create ChromeDriver directory
mkdir -p $CHROMEDRIVER_DIR

# Download specific ChromeDriver version for Chrome 131
CHROMEDRIVER_VERSION="131.0.6778.111"
echo "Using ChromeDriver version: $CHROMEDRIVER_VERSION"

wget -O "$CHROMEDRIVER_DIR/chromedriver.zip" "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip"
cd $CHROMEDRIVER_DIR
unzip -o chromedriver.zip
chmod +x chromedriver-linux64/chromedriver

# Print versions for verification
echo "Chrome version:"
$STORAGE_DIR/chrome/opt/google/chrome/google-chrome --version
echo "ChromeDriver path: $CHROMEDRIVER_DIR/chromedriver-linux64/chromedriver"

# Install Python dependencies

echo "Build completed successfully"