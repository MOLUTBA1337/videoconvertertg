import asyncio
import math
from tiktokdownloader import video
from aiogram import Router, F
from aiogram.filters import Command,CommandObject
from aiogram.types import Message,CallbackQuery,FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database.db import Users
from config import bot
import os
from buttons.button import main_buttons,main_menuss

from redactor import redact_video
class Amount(StatesGroup):
    q1 = State()

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message,command: CommandObject,state: FSMContext):
    text = '<b>Привет! 👋\n\nДобро пожаловать в наш видеоконвертер! Этот бот поможет вам легко конвертировать ваши видео в видео-заметки. 📹✨\n\nПросто отправьте мне видео, и я преобразую его в видео-заметку, которую вы сможете использовать в чате. Начните сейчас и наслаждайтесь простотой конвертации!</b>'
    Users(message.from_user.id).add_user()
    await message.answer(text=text,reply_markup=main_buttons())

@router.callback_query(F.data=='main_menu')
async def main_menu(call: CallbackQuery,state:FSMContext):
    await state.clear()
    await call.message.delete()
    text = '<b>Привет! 👋\n\nДобро пожаловать в наш видеоконвертер! Этот бот поможет вам легко конвертировать ваши видео в видеокружок. 📹✨\n\nПросто отправьте мне видео, и я преобразую его в видеокружок. Начните сейчас и наслаждайтесь простотой конвертации!</b>'
    await call.message.answer(text=text, reply_markup=main_buttons())


@router.callback_query(F.data=='profile')
async def profile(call: CallbackQuery):
    await call.message.delete()

    text = f'<b>👤 Пользователь:</b> @{call.from_user.username} (ID: {call.from_user.id})'
    await call.message.answer(text=text)



@router.message(F.video)
async def convert(message: Message):

    if message.video.duration > 60*3:
        await message.answer('<b>Видео длится больше 60 секунд!\n\nОтправьте видео длительностью не более 60 секунд!</b>')
        return

    else:
        if message.video.file_size/(2**20) > 20:
            await message.answer('<b>К сожалению телеграмм может скачивать файлы не более 20мб.\nИзмените качество для конвертации</b>')
            return


        first = await message.reply('<b>Это займет некоторое время!</b>')

        file_path = await bot.get_file(message.video.file_id)
        second = await bot.edit_message_text(text='<b>Видео скачивается!</b>',message_id=first.message_id,chat_id=message.from_user.id)
        await bot.download_file(file_path.file_path, destination=f"media/{message.from_user.id}_input_video.mp4",timeout=60)
        third = await bot.edit_message_text('<b>Видео обрабатывается!</b>',message_id=second.message_id,chat_id=message.from_user.id)
        redact_video(message.from_user.id)

        document = FSInputFile(f"media/{message.from_user.id}_output_video.mp4")
        await bot.delete_message(message_id=third.message_id,chat_id=message.from_user.id)
        Users(message.from_user.id).minus_count(1)
        await bot.send_video_note(message.from_user.id,video_note=document)

        if os.path.exists(f"media/{message.from_user.id}_input_video.mp4"):
            os.remove(f"media/{message.from_user.id}_input_video.mp4")
        if os.path.exists(f"media/{message.from_user.id}_output_video.mp4"):
            os.remove(f"media/{message.from_user.id}_output_video.mp4")



@router.message(F.text.startswith('https://vt.tiktok.com'))
@router.message(F.text.startswith('vt.tiktok.com'))
@router.message(F.text.startswith('https://www.tiktok.com'))
@router.message(F.text.startswith('www.tiktok.com'))
async def tiktok(message: Message):
    link = message.text
    video_status = video(message.from_user.id,link)
    if video_status != "Видео успешно скачано!":
        await message.answer(video_status)
    else:
        name = f"media/{message.from_user.id}_tiktok.mp4"
        document = FSInputFile(name)

        await message.answer_video(document)
        os.rename(f"media/{message.from_user.id}_tiktok.mp4",f"media/{message.from_user.id}_input_video.mp4")
        check = redact_video(message.from_user.id)
        if check is None:
            document = FSInputFile(f"media/{message.from_user.id}_input_video.mp4")
            await message.answer_video_note(document)
            if os.path.exists(f"media/{message.from_user.id}_input_video.mp4"):
                os.remove(f"media/{message.from_user.id}_input_video.mp4")
            if os.path.exists(f"media/{message.from_user.id}_output_video.mp4"):
                os.remove(f"media/{message.from_user.id}_output_video.mp4")







