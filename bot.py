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
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
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
    logger.info(f"Screenshot saved: {filename}")
    return filename

@bot.command(name='changeoutfit', cooldown_after=True, cooldown_rate=1, cooldown_per=3600)
async def changeoutfit(ctx):
    await ctx.send("Starting outfit change process...")
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            success = await bot.loop.run_in_executor(executor, run_selenium)
        if success:
            await ctx.send("Outfit change command sent successfully!")
        else:
            await ctx.send("Failed to send outfit command. Check logs.")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")
        logger.error(f"Error: {str(e)}\n{traceback.format_exc()}")

def run_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir=/tmp/chrome-profile-{uuid.uuid4()}")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    actions = ActionChains(driver)

    try:
        # Step 1: Go directly to bot URL
        bot_url = "https://app.fnlb.net/bot?id=6814b1d57fbd12fb94b67c8a"
        logger.info(f"Navigating to bot URL: {bot_url}")
        driver.get(bot_url)
        time.sleep(3)
        take_screenshot(driver, "initial_page")

        # Step 2: Check if login is required
        try:
            # Look for login elements
            email_field = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
            
            logger.info("Login required - proceeding with authentication")
            email_field.send_keys("baileyksmith2010@gmail.com")
            
            password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_field.send_keys("Boughton5")
            time.sleep(1)
            
            login_button = driver.find_element(By.XPATH, "//button[contains(., 'Login')]")
            login_button.click()
            time.sleep(5)
            take_screenshot(driver, "after_login")
            
            # After login, we should be back on the bot page
            driver.get(bot_url)
            time.sleep(3)
            
        except TimeoutException:
            logger.info("No login required - already authenticated")
            pass

        # Step 3: Send keyboard commands
        logger.info("Sending keyboard commands...")
        
        # Focus on page body
        body = driver.find_element(By.TAG_NAME, 'body')
        body.click()
        time.sleep(1)
        
        # Press 'c' to open chat
        actions.send_keys('c').perform()
        time.sleep(2)
        take_screenshot(driver, "after_pressing_c")
        
        # Type command
        actions.send_keys("outfit fishstick").perform()
        time.sleep(1)
        
        # Press Enter
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(2)
        take_screenshot(driver, "after_sending_command")

        return True

    except Exception as e:
        logger.error(f"Error during execution: {str(e)}\n{traceback.format_exc()}")
        take_screenshot(driver, "error_state")
        return False
    finally:
        driver.quit()

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
