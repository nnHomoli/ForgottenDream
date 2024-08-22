import requests.exceptions
import telebot

from config import TOKEN

bot = telebot.TeleBot(TOKEN)


def write_messageID(message=None, messageitself=None, uid=None):
    if message is not None:
        path = f'./chatIDmessageID/{message.from_user.id}.txt'
    else:
        if uid is not None:
            path = f'./chatIDmessageID/{uid}.txt'
    with open(path, 'a') as file:
        mid = messageitself.message_id
        file.write(f'{mid}\n')


def return_latest_messageID(message, uid=None):
    try:
        if uid is None:
            with open(f'./chatIDmessageID/{message.from_user.id}.txt', 'r') as latest:
                lines = latest.readlines()
        else:
            with open(f'./chatIDmessageID/{uid}.txt', 'r') as latest:
                lines = latest.readlines()
        latest_message = lines[-1]

        return latest_message
    except FileNotFoundError:
        return

def delete_old_messages(message=None, uid=None):
    try:
        if message is not None:
            chat_data_path = f'./chatIDmessageID/{message.from_user.id}.txt'
            with open(chat_data_path, 'r') as old_messages:
                useless_messages = old_messages.readlines()
                uid = message.from_user.id
    except FileNotFoundError:
        return

    if uid is not None:
        chat_data_path = f'./chatIDmessageID/{uid}.txt'
        with open(chat_data_path, 'r') as old_messages:
            useless_messages = old_messages.readlines()

    for message_id in useless_messages:
        delete_msg(uid=uid, message_id=message_id)

    with open(chat_data_path, 'w') as whyisitthere:
        whyisitthere.write('')


def delete_msg(uid, message_id):
    try:
        bot.delete_message(chat_id=uid, message_id=int(message_id))
    except Exception:
        if Exception == requests.exceptions:
            delete_msg(uid, message_id)
        else:
            pass