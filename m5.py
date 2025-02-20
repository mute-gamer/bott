import time
import asyncio
import random
import requests
import re
import threading
import schedule
import tweepy
from telegram import Bot
from flask import Flask
import os

port = int(os.environ.get("PORT", 10000))  

# Bot Config
TELEGRAM_BOT_TOKEN = "7817464511:AAFvpS58HxWAreM6uzhEVC_WHSj-qUdE4zw"
TELEGRAM_CHAT_ID = "-1002310803321"
CHANNEL_ID = "UC4mvivsBEX3Mq7us5U4lb7w"

# Twitter API v2 Config
API_KEY = "Ap2Ci84eE6vZUZKaAOiVelTBR"
API_SECRET = "C1cvyO6aGpMeUTl7ZhfqMS2E5aeOdNXQ3Z4bRBxexX068AY7aF"
ACCESS_TOKEN = "1892531779556294656-2RPN8Lzu1Y24ghsPMI4PrOkpG1Pfy5"
ACCESS_SECRET = "J1vjckTu1cLXVk07OtmNXDxQx65r7gI6ONCK3XKYRsRWk"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAANi0zQEAAAAAuxAISnNeAD4QFKnx9TDRoUEWfsM%3Dygg0532OyLSB63SA2rrHtZYIt8S4wiKtk1k5YV3XCei8ekkqGe"

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
twitter_api = tweepy.API(auth)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
last_post_id = None
last_video_id = None

def send_twitter_post(text):
    try:
        twitter_api.update_status(text)
        print("✅ Tweet posted successfully!")
    except tweepy.TweepyException as e:
        print(f"⚠️ Error posting Tweet: {e}")

async def send_telegram_message(text):
    try:
        await bot.send_message(TELEGRAM_CHAT_ID, text, parse_mode="HTML")
        send_twitter_post(text)  # Post same message on Twitter
    except Exception as e:
        print(f"⚠️ Error sending Telegram message: {e}")

async def send_promotion():
    messages = [
        "🚨 Don't miss out! Subscribe now and stay updated with the latest content! 🛎️🔥",
        "🔥 Join the adventure! Hit that subscribe button and become part of the family! 💥❤️",
    ]
    await send_telegram_message(f"{random.choice(messages)}\n\n👉 <a href='https://www.youtube.com/channel/{CHANNEL_ID}'>Subscribe Here</a>")

async def get_community_posts():
    global last_post_id
    url = f"https://www.youtube.com/channel/{CHANNEL_ID}/community"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        post_id_match = re.search(r'"postId":"(.*?)"', response.text)
        if post_id_match:
            post_id = post_id_match.group(1)
            post_url = f"https://www.youtube.com/post/{post_id}"
            if post_id != last_post_id:
                last_post_id = post_id
                await send_telegram_message(f"🔥 New Community Post!\n\n📰 <a href='{post_url}'>Check it out</a>")

async def get_latest_video():
    global last_video_id
    url = f"https://www.youtube.com/channel/{CHANNEL_ID}/videos"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        video_id_match = re.search(r'"videoId":"(.*?)"', response.text)
        if video_id_match:
            video_id = video_id_match.group(1)
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            if video_id != last_video_id:
                last_video_id = video_id
                await send_telegram_message(f"🎥 New Video Uploaded!\n\n🚀 <a href='{video_url}'>Watch Now</a>")

async def check_updates():
    while True:
        await get_latest_video()
        await get_community_posts()
        await asyncio.sleep(30)  # Check every 30 seconds

def schedule_promotion():
    schedule.every(1).hours.do(lambda: asyncio.create_task(send_promotion()))

async def schedule_loop():
    schedule_promotion()
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

async def main():
    asyncio.create_task(check_updates())
    await schedule_loop()

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(main())
