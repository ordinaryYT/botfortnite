import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

def run_selenium():
    # Generate a unique user data directory
    user_data_dir = f"/tmp/chrome-profile-{uuid.uuid4()}"

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={user_data_dir}")  # Specify unique user data dir
    options.add_argument("--headless")  # Run in headless mode for Render
    options.add_argument("--no-sandbox")  # Required for some environments like Render
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource issues

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)  # Increased timeout to 20 seconds

    try:
        driver.get("https://app.fnlb.net/")

        # Wait for and click Login button using JavaScript to bypass interception
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        driver.execute_script("arguments[0].click();", login_btn)

        # Wait for email input to be present and enter credentials
        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        email_input.send_keys("baileyksmith2010@gmail.com")

        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        password_input.send_keys("Boughton5")

        # Submit login using JavaScript to bypass interception
        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        driver.execute_script("arguments[0].click();", submit_btn)

        # Wait for dashboard to load, click My Bots
        my_bots = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'My bots')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", my_bots)
        driver.execute_script("arguments[0].click();", my_bots)

        # Search for OGsbot69
        search_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Search for a bot')]")))
        search_input.send_keys("OGsbot69")

        # Wait a bit for search results
        time.sleep(2)  # Adjust if needed

        # Click on "pub bots 1" using JavaScript
        pub_bots = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'pub bots 1')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", pub_bots)
        driver.execute_script("arguments[0].click();", pub_bots)

        # Click on OGsbot69 card using JavaScript
        ogs_bot = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'OGsbot69')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", ogs_bot)
        driver.execute_script("arguments[0].click();", ogs_bot)

        # Click Chat button using JavaScript
        chat_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Chat')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", chat_btn)
        driver.execute_script("arguments[0].click();", chat_btn)

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

@bot.command(name='changeoutfit')
async def change_outfit(ctx):
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

# Use environment variable for bot token
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
