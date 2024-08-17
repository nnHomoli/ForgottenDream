import requests.exceptions
import telebot
import os
import threading
from datetime import datetime, timedelta
from config import TOKEN, chat_path, gen_path

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


def message_fixer():
    while True:
        if not os.path.exists(chat_path):
            os.mkdir(chat_path)

        for filename in os.listdir(chat_path):
            try:
                if filename.endswith('.txt') and os.path.getsize(f'{chat_path}/{filename}') != 0:
                    uid = filename.replace('.txt', '')
                    last_modified = datetime.fromtimestamp(os.path.getmtime(f'{chat_path}/{filename}'))
                    current_time = datetime.now()
                    delta = current_time - last_modified

                    if delta >= timedelta(hours=48):
                        os.remove(f'{chat_path}/{filename}')

                    elif delta >= timedelta(hours=42):
                        delete_old_messages(uid=uid)
            except FileNotFoundError:
                pass


def data_assistant():
    while True:
        if not os.path.exists(gen_path):
            os.mkdir(gen_path)

        for filename in os.listdir(gen_path):
            if filename.endswith('..png'):
                try:
                    last_modified = datetime.fromtimestamp(os.path.getmtime(f'{gen_path}/{filename}'))
                    current_time = datetime.now()
                    delta = current_time - last_modified
                    if delta >= timedelta(hours=24):
                        os.remove(f'{gen_path}/{filename}')
                except FileNotFoundError:
                    pass


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
    except requests.exceptions:
        delete_msg(uid, message_id)


message_fixer_thread = threading.Thread(target=message_fixer).start()
data_assistant_thread = threading.Thread(target=data_assistant).start()
