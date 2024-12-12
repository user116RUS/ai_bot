from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

"""InlineKeyboards"""
UNIVERSAL_BUTTONS = InlineKeyboardMarkup()

back = InlineKeyboardButton(text="Назад в меню 🔙", callback_data="back")

UNIVERSAL_BUTTONS.add(back)

PAY_BUTTONS = InlineKeyboardMarkup()
pay = InlineKeyboardButton(text="Оплатить", pay=True)

PAY_BUTTONS.add(pay)

back_hub = InlineKeyboardButton(text="Назад", callback_data="back_hub")

LONGMESSAGE_BUTTONS = InlineKeyboardMarkup()

message = InlineKeyboardButton(text="Отправить сообщениями", callback_data="lngmsg_msg")
documents = InlineKeyboardButton(text="Засунуть в файл", callback_data="lngmsg_docs")

LONGMESSAGE_BUTTONS.add(message, documents)

DOCUMENT_BUTTONS = InlineKeyboardMarkup()

docx = InlineKeyboardButton(text="Использовать .docx", callback_data="documents_docx")
txt = InlineKeyboardButton(text="Засунуть в .txt", callback_data="documents_txt")
back_docs = InlineKeyboardButton(text="Назад", callback_data="documents_back")

DOCUMENT_BUTTONS.add(docx, txt, back_docs)


"""ReplyKeyboards"""
