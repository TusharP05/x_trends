from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = 'twitter_trends'
COLLECTION_NAME = 'trending_topics'

# Twitter Credentials
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')
TWITTER_EMAIL = os.getenv('TWITTER_EMAIL')
TWITTER_PHONE='7908118840'
# ProxyMesh Configuration
PROXY_USERNAME = os.getenv('PROXY_USERNAME')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')
PROXY_HOST = os.getenv('PROXY_HOST')
PROXY_PORT = os.getenv('PROXY_PORT')

# Chrome Configuration for Render
CHROME_PATH = '/usr/bin/google-chrome-stable' if 'RENDER' in os.environ else None