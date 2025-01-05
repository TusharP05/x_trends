from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB Configuration
MONGODB_URI = 'mongodb+srv://tusharparakh05:GWSjJggabCcZj65u@cluster0.ilgnu.mongodb.net/twitter_trends?retryWrites=true&w=majority&tls=true'
DB_NAME = 'twitter_trends'
COLLECTION_NAME = 'trending_topics'

# Twitter Credentials
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')
TWITTER_EMAIL = os.getenv('TWITTER_EMAIL')

# ProxyMesh Configuration
PROXY_USERNAME = os.getenv('PROXY_USERNAME')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')
PROXY_HOST = os.getenv('PROXY_HOST')
PROXY_PORT = os.getenv('PROXY_PORT')