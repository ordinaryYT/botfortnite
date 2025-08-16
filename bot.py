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
    format='%(asctime)s - %(levelname)s - %(message)s'
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
            await ctx.send("Failed to send outfit command.")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

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
        # Your existing working login code here
        driver.get("https://app.fnlb.net/")
        time.sleep(3)
        
        login_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Login')]")))
        login_btn.click()
        time.sleep(2)
        
        email = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        email.send_keys("baileyksmith2010@gmail.com")
        
        password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password.send_keys("Boughton5")
        time.sleep(1)
        
        submit = driver.find_element(By.XPATH, "//button[contains(., 'Login')]")
        submit.click()
        time.sleep(5)

        # Only new part - pure keyboard automation after login
        logger.info("Sending keyboard commands...")
        
        # Press 'c' key to open chat
        actions.send_keys('c').perform()
        time.sleep(1)
        
        # Type the command
        actions.send_keys("outfit fishstick").perform() 
        time.sleep(1)
        
        # Press Enter
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(2)
        
        return True

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return False
    finally:
        driver.quit()

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
