from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.dispatcher.filters.callback_data import CallbackData


# generate keyboard Builder
# -> admin keyboard
async def generate_admin_key():
    keyboard_admin = InlineKeyboardBuilder()
    keyboard_admin.add(
        InlineKeyboardButton(text="Все подписчики канала", url="https://docs.google.com/spreadsheets/d/114XIai40l0tug1Xi9WQpN1OTwkJOd6ScQVOoxfnT2ks/"),
        InlineKeyboardButton(text="Забанить пользователя", callback_data="kicked_member")
    )

    keyboard_admin.adjust(2, 1, repeat=True)
    return keyboard_admin.as_markup()


async def generate_change_key():
    change_key = InlineKeyboardBuilder()
    change_key.add(
        InlineKeyboardButton(text="Подтверждаю", callback_data="yes"),
        InlineKeyboardButton(text="Отмена", callback_data="no")
    )
    change_key.adjust(2, repeat=True)
    return change_key.as_markup()
