#!/usr/bin/env bash

set -o errexit

STORAGE_DIR=/opt/render/project/.render

if [[ ! -d $STORAGE_DIR/chrome ]]; then
   echo "...Downloading Chrome"
   mkdir -p $STORAGE_DIR/chrome
   cd $STORAGE_DIR/chrome
   wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
   rm ./google-chrome-stable_current_amd64.deb
   cd $HOME/project
else
   echo "...Using Chrome from cache"
fi

# Get exact Chrome version
CHROME_VERSION=$($STORAGE_DIR/chrome/opt/google/chrome/google-chrome --version | cut -d' ' -f3)
echo "Chrome version: $CHROME_VERSION"

# Download specific ChromeDriver version for Chrome 131
CHROMEDRIVER_VERSION="131.0.6778.111"
echo "Using ChromeDriver version: $CHROMEDRIVER_VERSION"

wget -O "chromedriver.zip" "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip"
unzip -o "chromedriver.zip"
chmod +x chromedriver-linux64/chromedriver
mv chromedriver-linux64/chromedriver /usr/local/bin/

# Print versions for verification
echo "Chrome version:"
$STORAGE_DIR/chrome/opt/google/chrome/google-chrome --version
echo "ChromeDriver version:"
chromedriver --version

# Install Python dependencies
pip install -r requirements.txt

echo "Build completed successfully"