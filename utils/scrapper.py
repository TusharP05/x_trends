from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import json
import time
import random
import os
from config.config import TWITTER_USERNAME, TWITTER_PASSWORD, TWITTER_EMAIL, PROXY_USERNAME, PROXY_PASSWORD, PROXY_HOST, PROXY_PORT

class TwitterScraper:
    def __init__(self, manual_verify_timeout=300):
        self.manual_verify_timeout = manual_verify_timeout
        self.setup_driver()

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        
        # Required options for Render deployment
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--start-maximized')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # For Render deployment
        if 'RENDER' in os.environ:
            options.binary_location = "/usr/bin/google-chrome"

        # ProxyMesh configuration -
        """
        PROXY_USERNAME = Config.PROXY_USERNAME
        PROXY_PASSWORD = Config.PROXY_PASSWORD
        PROXY_HOST = Config.PROXY_HOST
        PROXY_PORT = Config.PROXY_PORT
        options.add_argument(f'--proxy-server=http://{PROXY_HOST}:{PROXY_PORT}')
        options.add_argument(f'--proxy-auth={PROXY_USERNAME}:{PROXY_PASSWORD}')
        options.add_argument(f'--proxy-bypass-list=<-loopback>')
        """

        # Set user agent
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        
        self.driver.set_window_size(1920, 1080)
        
        # Add CDP commands
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def human_like_typing(self, element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

    def wait_for_manual_verification(self):
        print("\n=== VERIFICATION CODE REQUIRED ===")
        print("Waiting for verification...")
        
        initial_url = self.driver.current_url
        start_time = time.time()
        
        while time.time() - start_time < self.manual_verify_timeout:
            current_url = self.driver.current_url
            page_source = self.driver.page_source.lower()
            
            if current_url != initial_url and not any([
                x in current_url for x in ["verify", "verification", "confirm", "challenge", "authenticate"]
            ]):
                return True
                
            verification_indicators = [
                x in page_source for x in [
                    "verification", "verify", "confirmation",
                    "confirm your identity", "enter the code",
                    "verify your phone", "verify your email"
                ]
            ]
            
            if not any(verification_indicators):
                return True
                
            time.sleep(1)
            
        return False

    def check_for_verification(self):
        try:
            verification_elements = self.driver.find_elements(By.XPATH, 
                "//*[contains(text(), 'verification') or contains(text(), 'Verify') or \
                contains(text(), 'confirm') or contains(text(), 'Confirm') or \
                contains(text(), 'Enter the code')]"
            )
            if verification_elements and not self.wait_for_manual_verification():
                raise Exception("Verification timeout")
        except NoSuchElementException:
            pass
        return True

    def wait_for_element(self, by, value, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            return None

    def get_current_ip(self):
        try:
            self.driver.get("http://httpbin.org/ip")
            time.sleep(2)
            pre_element = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "pre"))
            )
            data = json.loads(pre_element.text)
            return data.get('origin', 'Unknown IP')
        except Exception as e:
            print(f"Error fetching IP: {e}")
            return "Unknown IP"

    def login(self):
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
                print('Current input:', input_type)

                if input_type == 'username':
                    self.handle_input_step('username', TWITTER_USERNAME)
                elif input_type == 'password':
                    self.handle_input_step('password', TWITTER_PASSWORD)
                elif input_type == 'email_or_phone':
                    self.handle_input_step('email_or_phone', TWITTER_EMAIL)
                elif input_type == 'phone_or_username':
                    self.handle_input_step('phone_or_username', TWITTER_USERNAME)
                elif input_type == 'verification':
                    if not self.wait_for_manual_verification():
                        return False
                else:
                    print("Unknown input type")
                    return False

                step_count += 1
                time.sleep(2)

            return self.is_home_page()

        except Exception as e:
            print(f"Login failed: {e}")
            return False

    def is_home_page(self):
        try:
            return any([
                'home' in self.driver.current_url.lower(),
                'feed' in self.driver.current_url.lower(),
                self.wait_for_element(By.CSS_SELECTOR, '[data-testid="primaryColumn"]', timeout=5) is not None
            ])
        except:
            return False

    def check_for_input_type(self):
        page_source = self.driver.page_source
        for text, input_type in [
            ('Enter your password', 'password'),
            ('Enter your phone number or email address', 'email_or_phone'),
            ('Enter your phone number or username', 'phone_or_username'),
            ('Sign in to X', 'username')
        ]:
            if text in page_source:
                return input_type
        if any(x in page_source.lower() for x in ['verification code', 'confirm your identity']):
            return 'verification'
        return None

    def handle_input_step(self, input_type, value):
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
        except Exception as e:
            print(f"Error handling {input_type}: {e}")
        return False

    def get_trending_topics(self):
        try:
            print("Navigating to Twitter trends...")
            self.driver.get("https://x.com/explore/tabs/trending")
            time.sleep(random.uniform(3, 5))
            
            print("Fetching trending topics...")
            page_html = self.driver.page_source
            soup = BeautifulSoup(page_html, "html.parser")
            trends = soup.find_all("div", {"data-testid": "trend"}, limit=5)
            
            trending_data = []
            for trend in trends:
                try:
                    topic_name = trend.find('div', class_='css-146c3p1 r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-b88u0q r-1bymd8e')
                    if topic_name:
                        trending_data.append(topic_name.get_text(strip=True))
                except Exception as e:
                    print(f"Error parsing trend: {e}")
                    
            print(f"Found {len(trending_data)} trending topics")
            return trending_data[:5]

        except Exception as e:
            print(f"Error fetching trends: {e}")
            return []

    def cleanup(self):
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
                print("Browser closed successfully")
        except Exception as e:
            print(f"Cleanup error: {e}")