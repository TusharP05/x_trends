# Twitter Trends Scraper

A web scraping application that automatically fetches the top 5 trending topics from Twitter/X using Selenium and stores them in MongoDB. Built with FastAPI for the backend API.

## Live Demo
The application is live at: [https://x-trends-1.onrender.com/](https://x-trends-1.onrender.com/)

## Features

- Automated Twitter login with support for two-factor authentication
- Scrapes top 5 trending topics from Twitter's trending page
- Stores results in MongoDB with timestamp and IP information
- Web interface to view and trigger scraping
- Support for proxy configuration (ProxyMesh)
- Deployed on Render with headless Chrome

## Tech Stack

- Python 3.9+
- Selenium WebDriver
- FastAPI
- MongoDB
- BeautifulSoup4
- ChromeDriver
- Render for deployment

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/twitter-trends-scraper.git
cd twitter-trends-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your credentials:
```env
TWITTER_USERNAME=your_username
TWITTER_PASSWORD=your_password
TWITTER_EMAIL=your_email
TWITTER_PHONE=your_phone
MONGODB_URI=your_mongodb_uri

# Optional ProxyMesh configuration
PROXY_USERNAME=your_proxymesh_username
PROXY_PASSWORD=your_proxymesh_password
PROXY_HOST=us-ca.proxymesh.com
PROXY_PORT=31280
```

## Project Structure

```
twitter_trends/
│
├── config/
│   ├── __init__.py
│   └── config.py           # Configuration settings
│
├── utils/
│   ├── __init__.py
│   └── scraper.py         # Twitter scraping functionality
│
├── static/                 # Static files
├── .env                   # Environment variables
├── .gitignore
├── build.sh              # Render build script
├── render.yaml           # Render configuration
├── requirements.txt      # Project dependencies
├── main.py              # FastAPI application
└── README.md
```

## Usage

### Local Development
1. Start the server:
```bash
uvicorn main:app --reload
```

2. Visit `http://localhost:8000` in your browser

3. Click the "Scrape Trends" button to fetch the latest trending topics

### Production Deployment
The application is deployed on Render and can be accessed at:
- [https://x-trends-1.onrender.com/](https://x-trends-1.onrender.com/)

## API Endpoints

- `GET /`: Web interface
- `GET /scrape`: Trigger scraping and return results

## Deployment on Render

The application is configured for deployment on Render with:
- Automatic Chrome and ChromeDriver installation
- Headless browser support
- Environment variable configuration
- Build and start scripts included

### Render Configuration
1. Connect your GitHub repository
2. Set up the following environment variables:
   - TWITTER_USERNAME
   - TWITTER_PASSWORD
   - TWITTER_EMAIL
   - TWITTER_PHONE
   - MONGODB_URI
3. Use the provided `build.sh` and `render.yaml` for deployment configuration

## Troubleshooting

Common issues and solutions:

1. Chrome/ChromeDriver version mismatch:
   - The build script automatically handles version matching

2. Proxy connection issues:
   - Check ProxyMesh credentials
   - Verify proxy server status

3. MongoDB connection:
   - Ensure IP whitelist includes Render's IP
   - Verify connection string format

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
