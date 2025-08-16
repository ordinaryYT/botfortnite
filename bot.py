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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def run_selenium():
    # Force fresh profile every time
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir=/tmp/chrome-profile-{uuid.uuid4()}")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    actions = ActionChains(driver)

    try:
        # Step 1: Navigate to FNLB
        logger.info("Loading FNLB...")
        driver.get("https://app.fnlb.net/")
        time.sleep(3)

        # Step 2: Click Login
        logger.info("Clicking login...")
        login_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Login')]")))
        login_btn.click()
        time.sleep(2)

        # Step 3: Enter credentials
        logger.info("Entering credentials...")
        email = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        email.send_keys("baileyksmith2010@gmail.com")
        
        password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password.send_keys("Boughton5")
        time.sleep(1)

        # Step 4: Submit login
        submit = driver.find_element(By.XPATH, "//button[contains(., 'Login')]")
        submit.click()
        time.sleep(5)

        # Step 5: Navigate directly to OGsbot6
        logger.info("Loading OGsbot6...")
        driver.get("https://app.fnlb.net/bot?id=6814b1d57fbd12fb94b67c8a")
        time.sleep(5)

        # Step 6: Keyboard commands
        logger.info("Sending commands...")
        actions.send_keys('c').perform()  # Open chat
        time.sleep(2)
        actions.send_keys("outfit fishstick").perform()  # Type command
        time.sleep(1)
        actions.send_keys(Keys.ENTER).perform()  # Send command
        time.sleep(3)

        return True

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return False
    finally:
        driver.quit()

@bot.command(name='changeoutfit')
async def changeoutfit(ctx):
    await ctx.send("Starting outfit change...")
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            success = await bot.loop.run_in_executor(executor, run_selenium)
        if success:
            await ctx.send("✅ Outfit command sent!")
        else:
            await ctx.send("❌ Failed to send command")
    except Exception as e:
        await ctx.send(f"💥 Error: {str(e)}")

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
