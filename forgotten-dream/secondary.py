import os

import misc
import queue
import telebot
import callbacks
import player_update
import messageManagment
import profileManagment
from fixer import Fixers
from telebot import types
from config import TOKEN, chat_path, user_data
from userDataManagment import ReadAndWrite

handler_queue = queue.Queue()

bot = telebot.TeleBot(TOKEN)
print(f"--//BOT: connected as {bot.get_me().username}")


@bot.message_handler(commands=['start'])
def start(message):
    user_data_path = f'{user_data}/[{message.from_user.id}].json'
    chat_data_path = f'{chat_path}/{message.from_user.id}.txt'

    if not os.path.exists(user_data_path):
        if os.path.exists(chat_data_path):
            messageManagment.delete_old_messages(message)

        kb = types.InlineKeyboardMarkup()
        ENg = types.InlineKeyboardButton(text='English', callback_data='SYSTEM: register_language English')
        RUs = types.InlineKeyboardButton(text='Русский', callback_data='SYSTEM: register_language Russian')
        NotAgree = types.InlineKeyboardButton(text='No/Нет', callback_data='SYSTEM: DeleteDataSure')

        kb.row(ENg, RUs)
        kb.row(NotAgree)

        caption = (
            'forgotten dream\n~~~~~~~~~~~~~~~~~~~|\n\n!!This game is experimental!!\n      If you wish to proceed, '
            'please select your preferred'
            'language. Otherwise, press "No" to delete first-step data\n\n!!Эта игра экспериментальна!!\n      Если '
            'вы хотите продолжить,'
            'выберите предпочитыемый язык, или в другом случае нажмите нет, чтобы удалить первоначальные '
            'данные\n\n')
        reply = bot.send_message(message.from_user.id, caption, reply_markup=kb, parse_mode='HTML')

        messageManagment.write_messageID(message, reply)

    else:
        messageManagment.delete_old_messages(message)
        misc.dialogue_box(message)

        caption = '<em>Loading...</em>'

        with open('./mapdev/mapFull.png', 'rb') as f:
            photo = f.read()

        reply = bot.send_photo(message.from_user.id, photo=photo, caption=caption, parse_mode='HTML')
        messageManagment.write_messageID(message, reply)
        player_update.move_player(message, (0, 0))


def register(call, language):
    registeruser = ReadAndWrite(call.from_user.id)
    reg_out = registeruser.register(language)

    if reg_out == "You've been successfully registered":
        start(call)


def create_new_slot(message, slot, loop=False):
    msgID = messageManagment.return_latest_messageID(message)

    lang = ReadAndWrite(message.from_user.id).read('language')

    caption = "<em>What's the name of your new Character?</em>" if lang == 'English' else (
        '<em>Какое имя вашего нового '
        'Персонажа?</em>')

    bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, parse_mode='HTML')
    bot.register_next_step_handler(message.message if not loop else message, profileManagment.create_new_slot_p2, slot, lang, msgID, start, create_new_slot)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.startswith("INGAME: "):
        callbacks.INGAME(call)

    elif call.data.startswith("DIALOGUE: "):
        callbacks.DIALOGUE(call)

    elif call.data.startswith("SYSTEM: "):
        out = call.data.replace("SYSTEM: ", "")

        if out.startswith('slotEMPTY'):
            create_new_slot(call, out.replace('slotEMPTY ', ''))

        elif out.startswith('register_language'):
            register(call, out.replace('register_language ', ''))

        else:
            callbacks.SYSTEM(call)

Fixers().start()

print("--//BOT: successfully started")
bot.infinity_polling()

