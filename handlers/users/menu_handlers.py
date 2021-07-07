import time
from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message

from keyboards.default.menu import menu
from keyboards.inline.choice_buttons import news_keyboard, date_keyboard, preview_keyboard, news_callback
from loader import dp, bot
from utils.publications import publications
from data.urls import urls


@dp.message_handler(Command(['start', 'menu', 'еню'], prefixes=['/', 'М', 'м']))
async def show_menu(message: types.Message):
    await enter_sections(message)


async def enter_sections(message: Union[CallbackQuery, Message], **kwargs):
    markup = await news_keyboard()
    if isinstance(message, Message):
        await message.answer(text="Выбери раздел:", reply_markup=markup)
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(reply_markup=markup)


async def enter_date(callback: CallbackQuery, section_name, **kwargs):
    markup = await date_keyboard(section_name)
    await callback.message.edit_text(text="Выбери период в днях:", reply_markup=markup)


async def enter_preview(callback: CallbackQuery, section_name, dater, **kwargs):
    markup = await preview_keyboard(section_name, dater)
    await callback.message.edit_text(text="Представление в ленте:", reply_markup=markup)


async def output_publications(callback: CallbackQuery, section_name, dater, preview):
    await callback.message.edit_reply_markup(reply_markup=None)
    url = urls.URL[section_name]
    all_pages_list = publications.main(dater=dater, url=url)
    for page in reversed(all_pages_list):
        for post_date, post_href_title in dict(reversed(page.items())).items():
            post_href = post_href_title[0]
            post_title = post_href_title[1]

            await bot.send_message(chat_id=callback.from_user.id,
                                   text=f'<b>{post_title}</b>\n<a href="{post_href}">link for more</a>',
                                   parse_mode="HTML",
                                   disable_web_page_preview=preview,
                                   reply_markup=menu)
            time.sleep(1)
    #await callback.message.answer(text="Для выбора раздела нажми \n /menu, либо воспользуйся меню ниже", reply_markup=menu)


@dp.callback_query_handler(text="cancel")
async def enter_cancel(callback: CallbackQuery):
    await callback.answer("Выбор отменен", show_alert=True)
    await callback.message.edit_reply_markup(reply_markup=None)


@dp.callback_query_handler(news_callback.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    section_name = callback_data.get("section_name")
    dater = callback_data.get("dater")
    preview = callback_data.get("preview")

    levels = {
        "0": enter_sections,
        "1": enter_date,
        "2": enter_preview,
        "3": output_publications
    }

    current_level_function = levels[current_level]

    await current_level_function(
        call,
        section_name=section_name,
        dater=dater,
        preview=preview
    )
