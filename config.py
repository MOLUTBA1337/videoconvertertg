from aiogram import Dispatcher,Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

admins = [6328214493]
token = "7771933584:AAElPcxJVXlo1MFlw-qt_Yj8BVHrh0-DIP8"

dp = Dispatcher()
bot = Bot(token=token,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
