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
    options.add_argument(f"user-data-dir={user_data_dir}")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)

    try:
        # Step 1: Navigate to FNLB
        logger.info("Navigating to FNLB...")
        driver.get("https://app.fnlb.net/")
        take_screenshot(driver, "initial_page_load")

        # Step 2: Click Login button
        logger.info("Clicking login button...")
        login_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'login')]")))
        driver.execute_script("arguments[0].click();", login_btn)
        time.sleep(2)
        take_screenshot(driver, "after_login_click")

        # Step 3: Enter credentials
        logger.info("Entering credentials...")
        email_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='email']")))
        email_input.clear()
        email_input.send_keys("baileyksmith2010@gmail.com")

        password_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='password']")))
        password_input.clear()
        password_input.send_keys("Boughton5")
        take_screenshot(driver, "credentials_entered")

        # Step 4: Submit login
        logger.info("Submitting login...")
        submit_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'login')]")))
        driver.execute_script("arguments[0].click();", submit_btn)
        time.sleep(5)
        take_screenshot(driver, "after_login_submit")

        # Step 5: Click My Bots
        logger.info("Clicking My Bots...")
        my_bots = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'my bots')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", my_bots)
        driver.execute_script("arguments[0].click();", my_bots)
        time.sleep(5)
        take_screenshot(driver, "after_mybots_click")

        # Step 6: Click search bar by fixed coordinates
        logger.info("Clicking search bar by coordinates...")
        take_screenshot(driver, "before_search_click_coords")

        # Get window size
        window_size = driver.get_window_size()
        win_width = window_size['width']
        win_height = window_size['height']

        # Adjust these percentages based on screenshot position
        search_x = int(win_width * 0.80)   # ~80% from left
        search_y = int(win_height * 0.13)  # ~13% from top

        actions = ActionChains(driver)
        actions.move_by_offset(search_x, search_y).click().perform()
        time.sleep(1)

        # Type into the search box
        actions.send_keys("OGsbot69").perform()
        time.sleep(2)
        take_screenshot(driver, "after_search_input_coords")

        # Step 7: Click on Pub bots 1
        logger.info("Clicking Pub bots 1...")
        pub_bots = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'pub bots 1')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", pub_bots)
        driver.execute_script("arguments[0].click();", pub_bots)
        time.sleep(3)
        take_screenshot(driver, "after_pub_bots_click")

        # Step 8: Click on OGsbot69
        logger.info("Clicking OGsbot69...")
        ogs_bot = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'ogsbot69')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", ogs_bot)
        driver.execute_script("arguments[0].click();", ogs_bot)
        time.sleep(2)
        take_screenshot(driver, "after_ogsbot_click")

        # Step 9: Click Chat button
        logger.info("Clicking Chat button...")
        chat_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'chat')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", chat_btn)
        driver.execute_script("arguments[0].click();", chat_btn)
        time.sleep(2)
        take_screenshot(driver, "after_chat_click")

        # Step 10: Send command
        logger.info("Sending command...")
        chat_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'run a command')]")))
        chat_input.send_keys("outfit fishstick")
        chat_input.send_keys(Keys.ENTER)
        time.sleep(2)
        take_screenshot(driver, "after_command_sent")

        driver.quit()
        return True

    except Exception as e:
        logger.error(f"BRUTE FORCE FAILED: {str(e)}\nStacktrace: {traceback.format_exc()}")
        
        if 'driver' in locals():
            try:
                logger.error(f"Current URL: {driver.current_url}")
                logger.error(f"Page title: {driver.title}")
                take_screenshot(driver, "final_error_state")
            except Exception as debug_error:
                logger.error(f"Failed to capture debug info: {str(debug_error)}")
            finally:
                driver.quit()
        
        return False

# Use environment variable for bot token
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
