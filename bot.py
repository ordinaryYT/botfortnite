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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

# Add cooldown: 1 hour (3600 seconds) per user
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

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)  # Increased timeout to 30 seconds

    try:
        driver.get("https://app.fnlb.net/")

        # Wait for and click Login button using JavaScript
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        driver.execute_script("arguments[0].click();", login_btn)
        time.sleep(2)  # Delay to avoid rapid requests

        # Wait for email input to be present and enter credentials
        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        email_input.send_keys("baileyksmith2010@gmail.com")

        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        password_input.send_keys("Boughton5")

        # Submit login using JavaScript
        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        driver.execute_script("arguments[0].click();", submit_btn)
        time.sleep(5)  # Increased delay after login

        # Wait for dashboard to load, click My Bots
        my_bots = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'My bots')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", my_bots)
        driver.execute_script("arguments[0].click();", my_bots)
        time.sleep(15)  # Increased delay for dashboard load to 15 seconds

        # Wait for the dashboard to fully load
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'My bots')]")))
        time.sleep(3)  # Additional delay for dynamic content

        # Retry loop for locating search input
        max_retries = 3
        search_input = None
        for attempt in range(max_retries):
            try:
                search_input = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Search') and contains(@placeholder, 'bot')]")
                if search_input.is_displayed():
                    break
            except NoSuchElementException:
                time.sleep(5)  # Wait 5 seconds before retrying
                if attempt == max_retries - 1:
                    logger.error(f"Page source after retries: {driver.page_source}")
                    raise TimeoutException("Could not find or display search input after retries")

        # Force search input using JavaScript
        driver.execute_script("arguments[0].value = 'OGsbot69';", search_input)
        driver.execute_script("arguments[0].dispatchEvent(new Event('input'));")  # Trigger input event
        time.sleep(2)  # Delay for search to process

        # Wait a bit for search results
        time.sleep(2)  # Adjust if needed

        # Click on "pub bots 1" using JavaScript
        pub_bots = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'pub bots 1')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", pub_bots)
        driver.execute_script("arguments[0].click();", pub_bots)
        time.sleep(2)

        # Click on OGsbot69 card using JavaScript
        ogs_bot = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'OGsbot69')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", ogs_bot)
        driver.execute_script("arguments[0].click();", ogs_bot)
        time.sleep(2)

        # Click Chat button using JavaScript
        chat_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Chat')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", chat_btn)
        driver.execute_script("arguments[0].click();", chat_btn)
        time.sleep(2)

        # Type command in chat
        chat_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Run a command')]")))
        chat_input.send_keys("outfit fishstick")
        chat_input.send_keys(Keys.ENTER)

        driver.quit()
        return True
    except Exception as e:
        error_msg = f"Error: {str(e)}\nStacktrace: {traceback.format_exc()}"
        logger.error(error_msg)  # Log to Render logs with ERROR level
        if 'driver' in locals():
            driver.quit()
        return False

# Use environment variable for bot token
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
