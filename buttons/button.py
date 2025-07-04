from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_buttons():


    buttons = [
        [
            types.InlineKeyboardButton(text="📣 Профиль", callback_data="profile")

        ],
        [
            types.InlineKeyboardButton(text="🆘 Support", url="https://t.me/softstocksupport")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def pay():


    buttons = [
        [
            types.InlineKeyboardButton(text="⬅️ Главное меню", callback_data="main_menu")

        ],
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard



def main_menuss():
    main = [

        [
            types.InlineKeyboardButton(text="⬅️ Главное меню", callback_data="main_menu")

        ]
    ]

    main_menus = types.InlineKeyboardMarkup(inline_keyboard=main)
    return main_menus


def adm_panels():

    adm = [
        [

            types.KeyboardButton(text="Рассылка")

        ],

        [

            types.KeyboardButton(text="Статистика")

        ],

    ]
    adm_panel = types.ReplyKeyboardMarkup(
        keyboard=adm,
        resize_keyboard=True
    )
    return adm_panel



