from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from buttons.button import adm_panels
from config import admins,bot
from database.db import Users
import asyncio
class Spam(StatesGroup):
    q1 = State()

class GiveGifts(StatesGroup):
    q1 = State()

class Marketing(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()

router = Router()

@router.message(Command('admin'))
async def panel_adm(message: Message):
    if message.from_user.id in admins:
        await message.answer('<b>Панель:</b>',reply_markup=adm_panels())

@router.message(F.text=='Рассылка')
async def spam(message: Message,state: FSMContext):
    if message.from_user.id in admins:
        await message.answer('Введите текст')
        await state.set_state(Spam.q1)

@router.message(Spam.q1)
async def spam1(message: Message,state: FSMContext):
    users = Users(message.from_user.id).return_users()
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0],from_chat_id=message.from_user.id,message_id=message.message_id)
            await asyncio.sleep(0.01)
        except:
            pass
    await state.clear()


@router.message(F.text=='Статистика')
async def statistics(message: Message):
    if message.from_user.id in admins:
        counts = len(Users(message.from_user.id).return_users())
        await message.answer(f'Кол-во юзеров в боте: {counts}')



