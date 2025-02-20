import time
import asyncio
import random
import requests
import re
import threading
import schedule
from telegram import Bot
from flask import Flask
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

port = int(os.environ.get("PORT", 10000))  

# Bot Config
TELEGRAM_BOT_TOKEN = "7817464511:AAFvpS58HxWAreM6uzhEVC_WHSj-qUdE4zw"
TELEGRAM_CHAT_ID = "-1002310803321"
CHANNEL_ID = "UC4mvivsBEX3Mq7us5U4lb7w"
USERNAME = "mute_g4mer"
PASSWORD = "20051384-Vajra"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
last_post_id = None
last_video_id = None

def send_twitter_post(text):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        driver.get("https://twitter.com/login")
        time.sleep(3)
        
        username_input = driver.find_element(By.NAME, "session[username_or_email]")
        password_input = driver.find_element(By.NAME, "session[password]")
        
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)
        
        driver.get("https://twitter.com/compose/tweet")
        time.sleep(3)
        
        tweet_box = driver.find_element(By.XPATH, "//div[@aria-label='Tweet text']")
        tweet_box.send_keys(text)
        
        tweet_button = driver.find_element(By.XPATH, "//div[@data-testid='tweetButtonInline']")
        tweet_button.click()
        
        time.sleep(3)
        driver.quit()
    except Exception as e:
        print(f"⚠️ Error sending Twitter post: {e}")

async def send_telegram_message(text):
    try:
        await bot.send_message(TELEGRAM_CHAT_ID, text, parse_mode="HTML")
    except Exception as e:
        print(f"⚠️ Error sending Telegram message: {e}")

async def send_promotion():
    messages = [
        "🚨 Don't miss out! Subscribe now and stay updated! 🛎️🔥",
        "🔥 Join the adventure! Hit that subscribe button! 💥❤️",
    ]
    await send_telegram_message(f"{random.choice(messages)}\n\n👉 <a href='https://www.youtube.com/channel/{CHANNEL_ID}'>Subscribe Here</a>")

def check_updates():
    while True:
        asyncio.run(get_latest_video())
        asyncio.run(get_community_posts())
        time.sleep(30)

def schedule_promotion():
    schedule.every(1).hours.do(lambda: asyncio.run(send_promotion()))

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    threading.Thread(target=check_updates, daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
