from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class WebAutomation:
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver with optimal settings"""
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✅ Chrome initialized with clean profile for reliable automation")
        except Exception as e:
            print(f"❌ Chrome setup failed: {e}")
            self.driver = None
    
    def google_search(self, query):
        """Perform Google search"""
        try:
            self.driver.get("https://www.google.com")
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            return f"Google search completed for: {query}"
        except Exception as e:
            return f"Google search failed: {e}"
    
    def youtube_search(self, query):
        """Search and play YouTube video"""
        try:
            # Ensure fresh driver for each search
            if not self.driver:
                self.setup_driver()
            
            self.driver.get("https://www.youtube.com")
            search_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "search_query"))
            )
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # Click first video
            time.sleep(3)
            first_video = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a#video-title"))
            )
            first_video.click()
            return f"YouTube video playing: {query}"
        except Exception as e:
            # Reset driver on failure
            self.setup_driver()
            return f"YouTube search failed: {e}"
    
    def whatsapp_send_message(self, contact, message):
        """Send WhatsApp message via web"""
        try:
            print(f"Opening WhatsApp Web to send message to {contact}...")
            self.driver.get("https://web.whatsapp.com")
            time.sleep(8)  # Wait for WhatsApp to load completely
            
            print("Searching for contact...")
            # Search contact - try multiple selectors
            search_selectors = [
                "//div[@contenteditable='true'][@data-tab='3']",
                "//div[@title='Search input textbox']",
                "//div[contains(@class, 'copyable-text') and @contenteditable='true']"
            ]
            
            search_box = None
            for selector in search_selectors:
                try:
                    search_box = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    break
                except:
                    continue
            
            if not search_box:
                return "Could not find search box"
            
            search_box.clear()
            search_box.send_keys(contact)
            time.sleep(3)
            
            print(f"Clicking on {contact}...")
            # Click contact - flexible selector
            contact_selectors = [
                f"//span[@title='{contact}']",
                f"//span[contains(text(), '{contact}')]",
                "//div[contains(@class, 'chat')]//span[1]"
            ]
            
            contact_element = None
            for selector in contact_selectors:
                try:
                    contact_element = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except:
                    continue
            
            if not contact_element:
                return f"Contact {contact} not found"
            
            contact_element.click()
            time.sleep(2)
            
            print("Sending message...")
            # Send message - try multiple selectors
            message_selectors = [
                "//div[@contenteditable='true'][@data-tab='10']",
                "//div[@title='Type a message']",
                "//div[contains(@class, 'copyable-text') and @contenteditable='true' and contains(@class, 'input')]"
            ]
            
            message_box = None
            for selector in message_selectors:
                try:
                    message_box = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    break
                except:
                    continue
            
            if not message_box:
                return "Could not find message input box"
            
            message_box.clear()
            message_box.send_keys(message)
            message_box.send_keys(Keys.RETURN)
            
            return f"WhatsApp message sent to {contact}: {message}"
            
        except Exception as e:
            return f"WhatsApp automation failed: {str(e)}"
    
    def gmail_compose(self, to_email, subject, body):
        """Compose Gmail"""
        try:
            self.driver.get("https://mail.google.com")
            time.sleep(5)  # Wait for login if needed
            
            # Click compose
            compose_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='button'][contains(text(),'Compose')]"))
            )
            compose_btn.click()
            
            # Fill email fields
            to_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "to"))
            )
            to_field.send_keys(to_email)
            
            subject_field = self.driver.find_element(By.NAME, "subjectbox")
            subject_field.send_keys(subject)
            
            body_field = self.driver.find_element(By.XPATH, "//div[@role='textbox']")
            body_field.send_keys(body)
            
            return f"Gmail composed to {to_email}"
        except Exception as e:
            return f"Gmail automation failed: {e}"
    
    def close_browser(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()

# Integration functions
web_bot = None

def init_web_automation():
    """Initialize web automation"""
    global web_bot
    if not web_bot or not web_bot.driver:
        web_bot = WebAutomation()
    return web_bot

def search_google(query):
    """Google search function"""
    bot = init_web_automation()
    return bot.google_search(query)

def search_youtube(query):
    """YouTube search function"""
    bot = init_web_automation()
    return bot.youtube_search(query)

def send_whatsapp_message(contact, message):
    """WhatsApp message function"""
    bot = init_web_automation()
    return bot.whatsapp_send_message(contact, message)

def compose_gmail(to_email, subject, body):
    """Gmail compose function"""
    bot = init_web_automation()
    return bot.gmail_compose(to_email, subject, body)

def close_web_automation():
    """Close web automation"""
    global web_bot
    if web_bot:
        web_bot.close_browser()
        web_bot = None