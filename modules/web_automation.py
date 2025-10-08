"""
Web Automation Module for AURA Assistant
Handles browser automation for Google, YouTube, Gmail, WhatsApp Web
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class WebAutomation:
    """Handles web browser automation tasks"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.logger.info("WebDriver initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
    
    def google_search(self, query):
        """Perform Google search"""
        try:
            if not self.driver:
                self.setup_driver()
            
            self.driver.get("https://www.google.com")
            
            # Find search box and enter query
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            self.logger.info(f"Google search performed for: {query}")
            return True
            
        except Exception as e:
            self.logger.error(f"Google search failed: {e}")
            return False
    
    def youtube_search(self, query):
        """Search and play video on YouTube"""
        try:
            if not self.driver:
                self.setup_driver()
            
            self.driver.get("https://www.youtube.com")
            
            # Find search box
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "search_query"))
            )
            
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results and click first video
            time.sleep(3)
            first_video = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a#video-title"))
            )
            first_video.click()
            
            self.logger.info(f"YouTube video played for: {query}")
            return True
            
        except Exception as e:
            self.logger.error(f"YouTube search failed: {e}")
            return False
    
    def compose_email(self, content):
        """Open Gmail and compose email"""
        try:
            if not self.driver:
                self.setup_driver()
            
            self.driver.get("https://mail.google.com")
            
            # Wait for Gmail to load and click compose
            compose_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and contains(text(), 'Compose')]"))
            )
            compose_button.click()
            
            # Wait for compose window and add content
            time.sleep(2)
            body_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Message Body']"))
            )
            body_field.send_keys(content)
            
            self.logger.info("Email composed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Email composition failed: {e}")
            return False
    
    def send_whatsapp(self, message, contact=None):
        """Send WhatsApp message via WhatsApp Web"""
        try:
            if not self.driver:
                self.setup_driver()
            
            self.driver.get("https://web.whatsapp.com")
            
            # Wait for WhatsApp Web to load (user needs to scan QR code)
            self.logger.info("Please scan QR code to login to WhatsApp Web")
            
            # Wait for main interface
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='chat-list']"))
            )
            
            if contact:
                # Search for specific contact
                search_box = self.driver.find_element(By.CSS_SELECTOR, "div[data-testid='chat-list-search']")
                search_box.click()
                search_input = self.driver.find_element(By.CSS_SELECTOR, "input[data-testid='search-input']")
                search_input.send_keys(contact)
                time.sleep(2)
                
                # Click first result
                first_contact = self.driver.find_element(By.CSS_SELECTOR, "div[data-testid='cell-frame-container']")
                first_contact.click()
            
            # Find message input and send message
            message_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='conversation-compose-box-input']"))
            )
            message_box.send_keys(message)
            message_box.send_keys(Keys.RETURN)
            
            self.logger.info("WhatsApp message sent successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"WhatsApp message failed: {e}")
            return False
    
    def open_website(self, url):
        """Open a specific website"""
        try:
            if not self.driver:
                self.setup_driver()
            
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            self.driver.get(url)
            self.logger.info(f"Opened website: {url}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to open website {url}: {e}")
            return False
    
    def close_browser(self):
        """Close the browser"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.logger.info("Browser closed")
                
        except Exception as e:
            self.logger.error(f"Failed to close browser: {e}")
    
    def take_screenshot(self, filename=None):
        """Take screenshot of current page"""
        try:
            if not self.driver:
                return None
            
            if not filename:
                filename = f"web_screenshot_{int(time.time())}.png"
            
            self.driver.save_screenshot(filename)
            self.logger.info(f"Web screenshot saved as {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Failed to take web screenshot: {e}")
            return None
    
    def scroll_page(self, direction="down", amount=3):
        """Scroll the page"""
        try:
            if not self.driver:
                return False
            
            if direction.lower() == "down":
                for _ in range(amount):
                    self.driver.execute_script("window.scrollBy(0, 300);")
            elif direction.lower() == "up":
                for _ in range(amount):
                    self.driver.execute_script("window.scrollBy(0, -300);")
            
            self.logger.info(f"Page scrolled {direction}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to scroll page: {e}")
            return False
    
    def go_back(self):
        """Navigate back in browser"""
        try:
            if self.driver:
                self.driver.back()
                self.logger.info("Navigated back")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to go back: {e}")
            return False
    
    def refresh_page(self):
        """Refresh current page"""
        try:
            if self.driver:
                self.driver.refresh()
                self.logger.info("Page refreshed")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to refresh page: {e}")
            return False