import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

def take_screenshot(driver, step_name):
    """Helper function to take screenshots for debugging"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{step_name}_{timestamp}.png"
    try:
        driver.save_screenshot(filename)
        logger.info(f"Screenshot saved: {filename}")
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
            await ctx.send("The command 'outfit fishstick' has been sent to OGsbot69.")
        else:
            await ctx.send("An error occurred while processing the outfit change. Check the server logs for details.")
    except Exception as e:
        await ctx.send(f"Unexpected error during execution: {str(e)}. Check the server logs for details.")
        logger.error(f"Unexpected error: {str(e)}\nStacktrace: {traceback.format_exc()}")

def run_selenium():
    # Generate a unique user data directory
    user_data_dir = f"/tmp/chrome-profile-{uuid.uuid4()}"

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={user_data_dir}")  # Specify unique user data dir
    options.add_argument("--headless")  # Run in headless mode for Render
    options.add_argument("--no-sandbox")  # Required for some environments like Render
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource issues
    options.add_argument("--disable-gpu")  # Improve rendering in headless mode
    options.add_argument("--window-size=1920,1080")  # Set window size

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 40)  # Increased timeout to 40 seconds

    try:
        # Step 1: Navigate to FNLB
        logger.info("Navigating to FNLB...")
        driver.get("https://app.fnlb.net/")
        take_screenshot(driver, "initial_page_load")

        # Step 2: Click Login button
        logger.info("Clicking login button...")
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        driver.execute_script("arguments[0].click();", login_btn)
        time.sleep(2)
        take_screenshot(driver, "after_login_click")

        # Step 3: Enter credentials
        logger.info("Entering credentials...")
        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        email_input.clear()
        email_input.send_keys("baileyksmith2010@gmail.com")

        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        password_input.clear()
        password_input.send_keys("Boughton5")
        take_screenshot(driver, "credentials_entered")

        # Step 4: Submit login
        logger.info("Submitting login...")
        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        driver.execute_script("arguments[0].click();", submit_btn)
        time.sleep(5)
        take_screenshot(driver, "after_login_submit")

        # Step 5: Click My Bots
        logger.info("Clicking My Bots...")
        my_bots = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'My bots')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", my_bots)
        driver.execute_script("arguments[0].click();", my_bots)
        time.sleep(10)
        take_screenshot(driver, "after_mybots_click")

        # Step 6: Search for bot
        logger.info("Searching for bot...")
        try:
            # Try multiple selector strategies for search input
            search_input = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//input[contains(@placeholder, 'Search')]")))
            
            logger.info(f"Search input attributes: placeholder='{search_input.get_attribute('placeholder')}', "
                      f"type='{search_input.get_attribute('type')}'")
            
            driver.execute_script("arguments[0].value = 'OGsbot69';", search_input)
            driver.execute_script("arguments[0].dispatchEvent(new Event('input'));")
            time.sleep(2)
            take_screenshot(driver, "after_search_input")
        except TimeoutException:
            logger.error("Failed to find search input. Current page source:")
            logger.error(driver.page_source[:2000])  # Log first 2000 chars of page source
            take_screenshot(driver, "search_input_timeout")
            raise

        # Step 7: Click on pub bots 1
        logger.info("Clicking pub bots 1...")
        pub_bots = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'pub bots 1')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", pub_bots)
        driver.execute_script("arguments[0].click();", pub_bots)
        time.sleep(2)
        take_screenshot(driver, "after_pub_bots_click")

        # Step 8: Click on OGsbot69
        logger.info("Clicking OGsbot69...")
        ogs_bot = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'OGsbot69')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", ogs_bot)
        driver.execute_script("arguments[0].click();", ogs_bot)
        time.sleep(2)
        take_screenshot(driver, "after_ogsbot_click")

        # Step 9: Click Chat button
        logger.info("Clicking Chat button...")
        chat_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Chat')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", chat_btn)
        driver.execute_script("arguments[0].click();", chat_btn)
        time.sleep(2)
        take_screenshot(driver, "after_chat_click")

        # Step 10: Send command
        logger.info("Sending command...")
        chat_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[contains(@placeholder, 'Run a command')]")))
        chat_input.send_keys("outfit fishstick")
        chat_input.send_keys(Keys.ENTER)
        time.sleep(2)
        take_screenshot(driver, "after_command_sent")

        driver.quit()
        return True

    except Exception as e:
        error_msg = f"Error at step: {logger.name}\nError: {str(e)}\nStacktrace: {traceback.format_exc()}"
        logger.error(error_msg)
        if 'driver' in locals():
            take_screenshot(driver, "error_state")
            driver.quit()
        return False

# Use environment variable for bot token
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
