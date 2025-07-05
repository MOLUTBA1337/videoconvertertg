from aiogram import Dispatcher,Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import os

load_dotenv()
admins = list(map(int,os.getenv("ADMIN").split(",")))
token = os.getenv("TOKEN")

dp = Dispatcher()
bot = Bot(token=token,default=DefaultBotProperties(parse_mode=ParseMode.HTML))


current_proccess = []