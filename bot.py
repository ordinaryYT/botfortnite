import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import asyncio
from selenium.webdriver.common.keys import Keys
from flask import Flask, send_file
import threading

# Flask server for showing browser state
app = Flask(__name__)
current_screenshot = None

@app.route('/')
def show_screenshot():
    if current_screenshot and os.path.exists(current_screenshot):
        return send_file(current_screenshot, mimetype='image/png')
    return "No active session", 404

def run_flask():
    app.run(host='0.0.0.0', port=5000)

# Start Flask in a separate thread
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def changeoutfit(ctx):
    global current_screenshot
    
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    if os.getenv('RENDER'):
        chrome_options.add_argument("--headless=new")
        chrome_options.binary_location = "/usr/bin/google-chrome"
        render_url = os.getenv('RENDER_EXTERNAL_URL', 'http://your-render-url.onrender.com')
    else:
        chrome_options.add_experimental_option("detach", True)
        render_url = "http://localhost:5000"
    
    # Enable remote debugging and video feed
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--window-size=1200,800")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Step 1: Navigate to FNLB
        await ctx.send(f"🌐 Starting browser session. View what's happening: {render_url}")
        driver.get("https://app.fnlb.net")
        
        # Save initial screenshot
        driver.save_screenshot("current.png")
        current_screenshot = "current.png"
        
        # Step 2: Manual login phase
        await ctx.send("🔐 **Manual Login Required**")
        await ctx.send("1. Visit the Render URL above to see the browser")
        await ctx.send("2. Complete the login and verification")
        await ctx.send("3. Type `!continue` when done")
        
        # Wait for continue command
        def check(m):
            return m.content == '!continue' and m.channel == ctx.channel and m.author == ctx.author
            
        try:
            await bot.wait_for('message', check=check, timeout=300)  # 5 minute timeout
        except asyncio.TimeoutError:
            await ctx.send("⏱️ Login timeout. Please try again.")
            return
            
        # Step 3: Automation after login
        await ctx.send("🤖 Resuming automation...")
        
        # Navigate to bot page
        driver.get("https://app.fnlb.net/bot?id=6814b1d57fbd12fb94b67c8a")
        time.sleep(3)
        
        # Execute commands
        body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))
        body.click()
        time.sleep(1)
        
        body.send_keys('c')
        time.sleep(2)
        
        for char in "outfit fishstick":
            body.send_keys(char)
            time.sleep(0.3)
            driver.save_screenshot("current.png")  # Update screenshot
        
        time.sleep(1)
        body.send_keys(Keys.ENTER)
        time.sleep(3)
        
        await ctx.send("✅ Command executed successfully!")
        driver.save_screenshot("result.png")
        await ctx.send(file=discord.File("result.png"))
        
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")
    finally:
        driver.quit()
        if os.path.exists("current.png"):
            os.remove("current.png")

@bot.command()
async def continue(ctx):
    """Dummy command to match the wait_for check"""
    pass

bot.run(os.getenv('DISCORD_TOKEN'))
