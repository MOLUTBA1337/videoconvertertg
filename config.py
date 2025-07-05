from aiogram import Dispatcher,Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import os

load_dotenv()
admins = 6328214493
token = "7771933584:AAGfPrcuvTAY44e6_m4LWGBwtAN8Cvil5e0"

dp = Dispatcher()
bot = Bot(token=token,default=DefaultBotProperties(parse_mode=ParseMode.HTML))


current_proccess = []