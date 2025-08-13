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
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://app.fnlb.net/")

        # Click Login button
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Login')]")))
        login_btn.click()

        # Enter email and password
        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        email_input.send_keys("baileyksmith2010@gmail.com")

        password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_input.send_keys("Boughton5")

        # Submit login
        submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        submit_btn.click()

        # Wait for dashboard to load, click My Bots
        my_bots = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'My bots')]")))
        my_bots.click()

        # Search for OGsbot69
        search_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Search for a bot')]")))
        search_input.send_keys("OGsbot69")

        # Wait a bit for search results
        time.sleep(2)  # Adjust if needed

        # Click on "pub bots 1"
        pub_bots = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'pub bots 1')]")))
        pub_bots.click()

        # Click on OGsbot69 card
        ogs_bot = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'OGsbot69')]")))
        ogs_bot.click()

        # Click Chat button
        chat_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Chat')]")))
        chat_btn.click()

        # Type command in chat
        chat_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Run a command')]")))
        chat_input.send_keys("outfit fishstick")
        chat_input.send_keys(Keys.ENTER)

        driver.quit()
        return True
    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        return False

@bot.command(name='changeoutfit')
async def change_outfit(ctx):
    await ctx.send("Starting outfit change process...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        success = await bot.loop.run_in_executor(executor, run_selenium)
    if success:
        await ctx.send("The command 'outfit fishstick' has been sent to OGsbot69.")
    else:
        await ctx.send("An error occurred while processing the outfit change.")

# Use environment variable for bot token
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
