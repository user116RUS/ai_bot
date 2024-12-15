from AI.settings import GROUP_ID
from bot import bot

from bot.core import is_message_forward_from, is_support_group, is_message_reply


def report_send(message):
    bot.forward_message(GROUP_ID, message.chat.id, message.message_id)

    # bot.send_message(chat_id=message.chat.id, text=e)

    bot.send_message(chat_id=message.chat.id, text="Ваша жалоба принята в обращение. Ожидайте.")


@is_support_group
@is_message_reply
def report_answer(message):
    original_message = message.reply_to_message

    if original_message.forward_from is not None:
        bot.send_message(chat_id=original_message.forward_from.id, text=message.text)
    else:
        print("0")