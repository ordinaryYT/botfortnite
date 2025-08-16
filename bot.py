import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time
import uuid
import concurrent.futures
import logging
import traceback
from datetime import datetime

# Enhanced logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Define intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def take_screenshot(driver, step_name):
    """Enhanced screenshot function with error handling"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{step_name}_{timestamp}.png"
        driver.save_screenshot(filename)
        logger.debug(f"Screenshot saved: {filename}")
        return filename
    except Exception as e:
        logger.error(f"Failed to take screenshot: {str(e)}")
        return None

@bot.command(name='changeoutfit', cooldown_after=True, cooldown_rate=1, cooldown_per=3600)
async def changeoutfit(ctx):
    await ctx.send("Starting outfit change process...")
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            success = await bot.loop.run_in_executor(executor, run_selenium)
        if success:
            await ctx.send("Outfit change command sent successfully!")
        else:
            await ctx.send("Failed to send outfit command. Check debug logs.")
    except Exception as e:
        await ctx.send(f"Critical error: {str(e)}")
        logger.critical(f"Command error: {str(e)}\n{traceback.format_exc()}")

def run_selenium():
    # Enhanced Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir=/tmp/chrome-profile-{uuid.uuid4()}")
    options.add_argument("--headless=new")  # New headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")
    
    # Enable performance logging
    options.set_capability("goog:loggingPrefs", {'performance': 'ALL', 'browser': 'ALL'})

    try:
        driver = webdriver.Chrome(options=options)
        actions = ActionChains(driver)
        logger.info("WebDriver initialized successfully")

        # Step 1: Login with enhanced waiting
        logger.debug("Navigating to FNLB...")
        driver.get("https://app.fnlb.net/")
        take_screenshot(driver, "initial_page")
        logger.debug(f"Current URL: {driver.current_url}")

        # Login process with explicit waits
        logger.debug("Attempting login...")
        try:
            login_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Login')]")))
            login_btn.click()
            logger.debug("Login button clicked")
            time.sleep(2)
            
            email = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
            email.send_keys("baileyksmith2010@gmail.com")
            logger.debug("Email entered")
            
            password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password.send_keys("Boughton5")
            logger.debug("Password entered")
            time.sleep(1)
            
            submit = driver.find_element(By.XPATH, "//button[contains(., 'Login')]")
            submit.click()
            logger.debug("Login submitted")
            
            # Wait for login to complete
            WebDriverWait(driver, 20).until(
                lambda d: "dashboard" in d.current_url.lower())
            logger.info("Login successful")
            take_screenshot(driver, "after_login")
            
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            take_screenshot(driver, "login_failed")
            raise

        # Step 2: Keyboard interaction with retries
        logger.info("Starting keyboard interaction...")
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                logger.debug(f"Keyboard attempt {attempt}/{max_retries}")
                
                # Focus on page body to ensure key events are captured
                driver.find_element(By.TAG_NAME, 'body').click()
                time.sleep(1)
                
                # Send 'c' key with explicit focus
                logger.debug("Sending 'c' key")
                actions.send_keys('c').perform()
                time.sleep(2)
                take_screenshot(driver, f"post_c_key_attempt_{attempt}")
                
                # Send command
                logger.debug("Typing command")
                actions.send_keys("outfit fishstick").perform()
                time.sleep(1)
                
                # Send Enter
                logger.debug("Sending Enter key")
                actions.send_keys(Keys.ENTER).perform()
                time.sleep(3)
                take_screenshot(driver, f"post_command_attempt_{attempt}")
                
                logger.info("Keyboard commands sent successfully")
                break
                
            except Exception as e:
                logger.warning(f"Attempt {attempt} failed: {str(e)}")
                if attempt == max_retries:
                    raise
                time.sleep(3)  # Wait before retry

        # Final verification
        time.sleep(5)
        take_screenshot(driver, "final_state")
        logger.info("Process completed successfully")
        return True

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}\n{traceback.format_exc()}")
        # Capture browser logs if available
        try:
            logs = driver.get_log('browser')
            logger.debug(f"Browser logs: {logs}")
            perf_logs = driver.get_log('performance')
            logger.debug(f"Performance logs: {perf_logs[:10]}")  # First 10 entries
        except Exception as log_error:
            logger.warning(f"Couldn't get browser logs: {str(log_error)}")
        
        take_screenshot(driver, "error_final")
        return False

    finally:
        if 'driver' in locals():
            try:
                driver.quit()
                logger.info("WebDriver closed successfully")
            except Exception as e:
                logger.error(f"Error closing driver: {str(e)}")

# Run bot with error handling
try:
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))
except Exception as e:
    logger.critical(f"Bot crashed: {str(e)}\n{traceback.format_exc()}")
