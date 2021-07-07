from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.urls import urls

news_callback = CallbackData("news", "level", "section_name", "dater", "preview")


def make_callback_data(level, section_name=0, dater=0, preview=False):
    return news_callback.new(level=level, section_name=section_name, dater=dater, preview=preview)


async def news_keyboard():
    CURRENT_LEVEL = 0

    markup = InlineKeyboardMarkup(row_width=2)

    sections = urls.URL
    for section_name, url in sections.items():
        text_button = f"{section_name}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           section_name=section_name, )

        markup.insert(InlineKeyboardButton(text=text_button,
                                           callback_data=callback_data))

    markup.row(
        InlineKeyboardButton(text="Отмена",
                             callback_data="cancel")
    )
    return markup


async def date_keyboard(section_name):
    CURRENT_LEVEL = 1

    markup = InlineKeyboardMarkup(row_width=1)

    number_of_days = 3
    for n in range(1, number_of_days+1):
        text_button = f"{n}"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           section_name=section_name,
                                           dater=n)
        markup.insert(InlineKeyboardButton(text=text_button,
                                           callback_data=callback_data))

    markup.row(
        InlineKeyboardButton(text="Назад",
                             callback_data=make_callback_data(level=CURRENT_LEVEL - 1))
    )

    markup.row(
        InlineKeyboardButton(text="Отмена",
                             callback_data="cancel")
    )

    return markup


async def preview_keyboard(section_name, dater):
    CURRENT_LEVEL = 2

    markup = InlineKeyboardMarkup(row_width=1)

    markup.insert(InlineKeyboardButton(text="Заголовок и превью",
                                       callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                                                        section_name=section_name,
                                                                        dater=dater, preview=False)))
    markup.insert(InlineKeyboardButton(text="Только заголовок",
                                       callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                                                        section_name=section_name,
                                                                        dater=dater, preview=True)))
    markup.row(
        InlineKeyboardButton(text="Назад",
                             callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                              section_name=section_name))
    )

    markup.row(
        InlineKeyboardButton(text="Отмена",
                             callback_data="cancel")
    )

    return markup
