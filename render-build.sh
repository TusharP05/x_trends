#!/usr/bin/env bash

# exit on error
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

# Download ChromeDriver
CHROME_VERSION=$($STORAGE_DIR/chrome/opt/google/chrome/google-chrome --version | cut -d' ' -f3 | cut -d'.' -f1)
CHROMEDRIVER_URL=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
CHROMEDRIVER_DOWNLOAD="https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_URL/chromedriver_linux64.zip"

echo "Downloading ChromeDriver version: $CHROMEDRIVER_URL"
wget -O "chromedriver.zip" "$CHROMEDRIVER_DOWNLOAD"
unzip -o "chromedriver.zip"
chmod +x chromedriver
mv chromedriver /usr/local/bin/

# Print versions
echo "Chrome version:"
$STORAGE_DIR/chrome/opt/google/chrome/google-chrome --version
echo "ChromeDriver version:"
chromedriver --version

# Install Python dependencies
pip install -r requirements.txt

echo "Build completed successfully"