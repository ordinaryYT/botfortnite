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

# Configure logging
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
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{step_name}_{timestamp}.png"
    driver.save_screenshot(filename)
    logger.debug(f"Screenshot saved: {filename}")
    return filename

@bot.command(name='changeoutfit', cooldown_after=True, cooldown_rate=1, cooldown_per=3600)
async def changeoutfit(ctx):
    await ctx.send("Starting outfit change process...")
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            success = await bot.loop.run_in_executor(executor, run_selenium)
        if success:
            await ctx.send("✅ Outfit command successfully executed!")
        else:
            await ctx.send("❌ Failed to send command. Check logs.")
    except Exception as e:
        await ctx.send(f"💥 Critical error: {str(e)}")
        logger.critical(f"Command error: {str(e)}\n{traceback.format_exc()}")

def run_selenium():
    # Configure Chrome to force fresh login
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")  # Fresh session every time
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    actions = ActionChains(driver)

    try:
        # Step 1: Navigate to bot URL
        bot_url = "https://app.fnlb.net/bot?id=6814b1d57fbd12fb94b67c8a"
        logger.info(f"Navigating to: {bot_url}")
        driver.get(bot_url)
        take_screenshot(driver, "01_initial_page")

        # Step 2: Force fresh login (always attempt)
        logger.info("Starting forced login...")
        try:
            # Wait for email field
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
            
            # Clear and enter credentials
            email_field.clear()
            email_field.send_keys("baileyksmith2010@gmail.com")
            
            password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_field.clear()
            password_field.send_keys("Boughton5")
            take_screenshot(driver, "02_credentials_entered")

            # Click login
            login_button = driver.find_element(By.XPATH, "//button[contains(., 'Login')]")
            login_button.click()
            logger.info("Login submitted")

            # Wait for bot page to reload
            WebDriverWait(driver, 20).until(
                lambda d: "bot?id=" in d.current_url)
            take_screenshot(driver, "03_post_login")
            time.sleep(3)  # Additional buffer

        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            take_screenshot(driver, "ERROR_login_failed")
            raise

        # Step 3: Keyboard command sequence
        logger.info("Executing keyboard commands...")
        
        # Focus on page
        driver.find_element(By.TAG_NAME, 'body').click()
        time.sleep(1)
        
        # Press 'c' to open chat
        actions.send_keys('c').perform()
        time.sleep(2)
        take_screenshot(driver, "04_after_pressing_c")
        
        # Type command slowly
        for char in "outfit fishstick":
            actions.send_keys(char).perform()
            time.sleep(0.2)  # Slower typing
        time.sleep(1)
        
        # Press Enter
        actions.send_keys(Keys.ENTER).perform()
        logger.info("Command submitted")
        time.sleep(3)
        take_screenshot(driver, "05_final_state")

        return True

    except Exception as e:
        logger.error(f"Execution failed: {str(e)}\n{traceback.format_exc()}")
        take_screenshot(driver, "ERROR_final_state")
        return False
    finally:
        driver.quit()
        logger.info("Browser closed")

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
