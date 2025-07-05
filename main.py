import asyncio
from use import admin,user
from config import dp,bot
from flask import Flask
import threading
import asyncio
import os

app = Flask(__name__)


@app.route('/')
def home():
    return "Bot is running!"


def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))


def keep_alive():
    for filename in os.listdir("media"):
        if filename.endswith(".mp4"):
            file_path = os.path.join("media", filename)
            os.remove(file_path)
    server = threading.Thread(target=run)
    server.start()




async def main():

    dp.include_routers(admin.router, user.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    keep_alive()
    asyncio.run(main())
