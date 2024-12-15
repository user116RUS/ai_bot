from AI.settings import GROUP_ID
from bot import bot

from bot.core import is_message_forward_from, is_support_group, is_message_reply


def report_send(message):
    bot.forward_message(GROUP_ID, message.chat.id, message.message_id)

    # bot.send_message(chat_id=message.chat.id, text=e)

    bot.send_message(chat_id=message.chat.id, text="Ваша жалоба принята в обращение. Ожидайте.")


def report_answer(message):
    try:
        if int(message.chat.id) == int(GROUP_ID):
            if message.reply_to_message is not None:
                original_message = message.reply_to_message
                print(original_message)
                if original_message.forward_origin is not None:
                    print("f")
                    print(original_message.forward_origin)
                    bot.send_message(chat_id=original_message.from_id, text=message.text)
                else:
                    print("0")
        else:
            print("no")
    except Exception as e:
        print(e)
        return
