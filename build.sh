#!/bin/bash

set -o errexit

STORAGE_DIR=/opt/render/project/.render

if [[ ! -d $STORAGE_DIR/chrome ]]; then
   echo "...Downloading Chrome"
   mkdir -p $STORAGE_DIR/chrome
   cd $STORAGE_DIR/chrome
   
   # Download Chrome .deb package
   wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   
   # Extract Chrome package
   dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
   
   # Remove the downloaded .deb file
   rm ./google-chrome-stable_current_amd64.deb
   
   # Return to original directory
   cd $HOME/project
else
   echo "...Using Chrome from cache"
fi

# Download ChromeDriver
CHROME_VERSION=$($STORAGE_DIR/chrome/opt/google/chrome/google-chrome --version | cut -d' ' -f3 | cut -d'.' -f1)
CHROMEDRIVER_URL=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
CHROMEDRIVER_DOWNLOAD="https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_URL/chromedriver_linux64.zip"

echo "Downloading ChromeDriver version: $CHROMEDRIVER_URL"
mkdir -p /opt/render/project/src/.render/
wget -O "/opt/render/project/src/.render/chromedriver.zip" "$CHROMEDRIVER_DOWNLOAD"

# Extract ChromeDriver
unzip -o "/opt/render/project/src/.render/chromedriver.zip" -d /opt/render/project/src/.render/
chmod +x /opt/render/project/src/.render/chromedriver

# Print versions for verification
echo "Chrome version:"
$STORAGE_DIR/chrome/opt/google/chrome/google-chrome --version

echo "ChromeDriver version:"
/opt/render/project/src/.render/chromedriver --version

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

echo "Build process completed successfully"