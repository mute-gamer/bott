import time
import asyncio
import random
import requests
import re
import threading
import schedule
import praw  # Reddit API Library
from telegram import Bot
from flask import Flask
import os

port = int(os.environ.get("PORT", 10000))  

# Bot Config
TELEGRAM_BOT_TOKEN = "7817464511:AAFvpS58HxWAreM6uzhEVC_WHSj-qUdE4zw"
TELEGRAM_CHAT_ID = "-1002310803321"
CHANNEL_ID = "UC4mvivsBEX3Mq7us5U4lb7w"

# Reddit API Config
REDDIT_CLIENT_ID = "vWjAJs-aDw0zhOFBh_aH8A"
REDDIT_CLIENT_SECRET = "f8k6Cy88rAU-8HfjWPD5wl4ZTd5NuA"
REDDIT_USERNAME = "mute031gamer@gmail.com"
REDDIT_PASSWORD = "20051384-Vajra"
USER_AGENT = "script:youtube_poster:v1.0 (by /u/Mute-Gamer)"
SUBREDDITS = ["gaming", "pcgaming", "gamers", "truegaming", "IndieGaming"]

bot = Bot(token=TELEGRAM_BOT_TOKEN)
last_post_id = None
last_video_id = None

# Reddit Login
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
    user_agent=USER_AGENT
)

def post_to_reddit(title, url):
    try:
        subreddit = random.choice(SUBREDDITS)  # انتخاب تصادفی یک ساب‌ردیت
        reddit.subreddit(subreddit).submit(title, url=url)
        print(f"✅ Posted to Reddit: {subreddit}")
    except Exception as e:
        print(f"⚠️ Error posting to Reddit: {e}")

async def send_telegram_message(text):
    try:
        await bot.send_message(TELEGRAM_CHAT_ID, text, parse_mode="HTML")
    except Exception as e:
        print(f"⚠️ Error sending Telegram message: {e}")

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
                post_to_reddit("Check out this awesome gaming video!", video_url)

def check_updates():
    while True:
        asyncio.run(get_latest_video())
        time.sleep(30)  # هر ۳۰ ثانیه چک کنه

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
