from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import json
import time
import random
import os
import shutil

# Import credentials from config
from config.config import TWITTER_USERNAME, TWITTER_PASSWORD, TWITTER_EMAIL

class TwitterScraper:
    def __init__(self, manual_verify_timeout=300):
        self.manual_verify_timeout = manual_verify_timeout
        self.driver = None
        self.wait = None
        self.setup_driver()

    def setup_driver(self):
        # Comprehensive Chrome binary search paths
        chrome_paths = [
            os.environ.get('CHROME_PATH', ''),
            '/opt/render/project/src/.render/chrome/google-chrome',
            '/opt/render/project/src/.render/chrome/chrome',
            '/opt/google/chrome/google-chrome',
            '/usr/bin/google-chrome',
            shutil.which('google-chrome'),
            '/usr/local/bin/google-chrome'
        ]
        
        # Comprehensive ChromeDriver search paths
        chromedriver_paths = [
            os.environ.get('CHROMEDRIVER_PATH', ''),
            '/opt/render/project/src/.render/chromedriver',
            '/usr/local/bin/chromedriver',
            '/usr/bin/chromedriver',
            shutil.which('chromedriver')
        ]
        
        # Find Chrome binary
        chrome_binary = None
        for path in chrome_paths:
            if path and os.path.exists(path) and os.access(path, os.X_OK):
                chrome_binary = path
                break
        
        # Find ChromeDriver
        chromedriver_path = None
        for path in chromedriver_paths:
            if path and os.path.exists(path) and os.access(path, os.X_OK):
                chromedriver_path = path
                break
        
        # Detailed error logging
        if not chrome_binary:
            print("CRITICAL: Chrome binary not found. Searched paths:")
            for path in chrome_paths:
                print(f"- {path}: {'EXISTS' if path and os.path.exists(path) else 'PATH EMPTY'}")
            raise Exception(f"Chrome binary not found. Searched paths: {chrome_paths}")
        
        if not chromedriver_path:
            print("CRITICAL: ChromeDriver not found. Searched paths:")
            for path in chromedriver_paths:
                print(f"- {path}: {'EXISTS' if path and os.path.exists(path) else 'PATH EMPTY'}")
            raise Exception(f"ChromeDriver not found. Searched paths: {chromedriver_paths}")
        
        # Selenium options setup
        options = webdriver.ChromeOptions()
        options.binary_location = chrome_binary
        
        # Extensive logging
        print(f"Using Chrome binary: {chrome_binary}")
        print(f"Using ChromeDriver: {chromedriver_path}")
        
        # Headless and other options
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--single-process')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Configure service
        service = Service(executable_path=chromedriver_path)
        
        try:
            # Initialize WebDriver
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 20)
            print("Chrome driver initialized successfully")
        except Exception as e:
            print(f"CRITICAL: WebDriver initialization failed: {e}")
            import traceback
            print(traceback.format_exc())
            raise

    def human_like_typing(self, element, text):
        """Simulate human-like typing with random delays between keystrokes."""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present with a specified timeout."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            print(f"Timeout waiting for element: {value}")
            return None

    def get_current_ip(self):
        """Fetch the current IP address."""
        try:
            print("Fetching current IP address...")
            self.driver.get("http://httpbin.org/ip")
            time.sleep(2)
            
            pre_element = self.wait_for_element(By.TAG_NAME, "pre")
            if pre_element:
                data = json.loads(pre_element.text)
                ip = data.get('origin', 'Unknown IP')
                print(f"Current IP: {ip}")
                return ip
            return "Unknown IP"
        except Exception as e:
            print(f"Error fetching IP: {e}")
            return "Unknown IP"

    def login(self):
        """Attempt to log in to Twitter/X."""
        try:
            print("Navigating to Twitter login...")
            self.driver.get("https://x.com/i/flow/login")
            max_steps = 5
            step_count = 0

            while step_count < max_steps:
                time.sleep(3)
                if self.is_home_page():
                    print("Successfully logged in!")
                    return True

                input_type = self.check_for_input_type()
                print(f'Current input field: {input_type}')

                success = False
                if input_type == 'username':
                    success = self.handle_input_step('username', TWITTER_USERNAME)
                elif input_type == 'password':
                    success = self.handle_input_step('password', TWITTER_PASSWORD)
                elif input_type == 'email_or_phone':
                    success = self.handle_input_step('email_or_phone', TWITTER_EMAIL)
                elif input_type == 'phone_or_username':
                    success = self.handle_input_step('phone_or_username', TWITTER_USERNAME)
                elif input_type == 'verification':
                    print("Verification required - not supported in headless mode")
                    return False
                else:
                    print("Unknown input type encountered")
                    return False

                if not success:
                    print(f"Failed to handle {input_type} input")
                    return False

                step_count += 1
                time.sleep(2)

            return self.is_home_page()

        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False

    def is_home_page(self):
        """Check if the current page is the home/feed page."""
        try:
            return any([
                'home' in self.driver.current_url.lower(),
                'feed' in self.driver.current_url.lower(),
                self.wait_for_element(By.CSS_SELECTOR, '[data-testid="primaryColumn"]', timeout=5) is not None
            ])
        except Exception as e:
            print(f"Error checking home page: {str(e)}")
            return False

    def check_for_input_type(self):
        """Determine the current input field type during login."""
        page_source = self.driver.page_source.lower()
        
        input_types = {
            'enter your password': 'password',
            'enter your phone number or email address': 'email_or_phone',
            'enter your phone number or username': 'phone_or_username',
            'sign in to x': 'username'
        }

        for text, input_type in input_types.items():
            if text in page_source:
                return input_type

        verification_phrases = ['verification code', 'confirm your identity']
        if any(phrase in page_source for phrase in verification_phrases):
            return 'verification'

        return None

    def handle_input_step(self, input_type, value):
        """Handle different input steps during login process."""
        input_selectors = {
            'password': 'input[name="password"]',
            'email_or_phone': 'input[data-testid="ocfEnterTextTextInput"]',
            'phone_or_username': 'input[data-testid="ocfEnterTextTextInput"]',
            'username': 'input[autocomplete="username"]'
        }
        
        try:
            print(f"Handling {input_type} input...")
            input_field = self.wait_for_element(By.CSS_SELECTOR, input_selectors[input_type])
            
            if input_field:
                self.human_like_typing(input_field, value)
                time.sleep(random.uniform(0.5, 1.5))
                input_field.send_keys(Keys.ENTER)
                time.sleep(3)
                return True
                
            print(f"Input field for {input_type} not found")
            return False
            
        except Exception as e:
            print(f"Error handling {input_type} input: {str(e)}")
            return False

    def get_trending_topics(self):
        """Scrape trending topics from Twitter/X."""
        try:
            print("Navigating to Twitter trends page...")
            self.driver.get("https://x.com/explore/tabs/trending")
            time.sleep(random.uniform(3, 5))
            
            print("Processing page content...")
            page_html = self.driver.page_source
            soup = BeautifulSoup(page_html, "html.parser")
            trends = soup.find_all("div", {"data-testid": "trend"}, limit=5)
            
            trending_data = []
            for trend in trends:
                try:
                    # Try multiple possible class names for trend topics
                    selectors = [
                        'css-901oao r-1nao33i r-37j5jr r-n6v787',
                        'css-1dbjc4n r-1nao33i r-37j5jr r-n6v787',
                        'css-146c3p1 r-bcqeeo r-qvutc0 r-37j5jr'
                    ]
                    
                    topic_name = None
                    for selector in selectors:
                        topic_name = trend.find('div', class_=selector)
                        if topic_name:
                            break
                    
                    if topic_name:
                        trend_text = topic_name.get_text(strip=True)
                        trending_data.append(trend_text)
                        print(f"Found trend: {trend_text}")
                        
                except Exception as e:
                    print(f"Error parsing individual trend: {str(e)}")
                    continue
            
            print(f"Successfully found {len(trending_data)} trending topics")
            return trending_data[:5]

        except Exception as e:
            print(f"Error fetching trends: {str(e)}")
            return []

    def cleanup(self):
        """Close the browser and clean up resources."""
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
                print("Browser closed successfully")
        except Exception as e:
            print(f"Cleanup error: {str(e)}")

    def __del__(self):
        """Destructor to ensure browser is closed when object is deleted."""
        self.cleanup()