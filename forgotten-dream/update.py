import telebot
import localization
import messageManagment
from misc import get_shm_name
from multiprocessing import shared_memory
from userDataManagment import ReadAndWrite
from telebot import types
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

shm = shared_memory.SharedMemory(name=get_shm_name())


move_down = types.InlineKeyboardButton(text='⬇️', callback_data='INGAME: down')
down_left = types.InlineKeyboardButton(text='/', callback_data='INGAME: down-left')
down_right = types.InlineKeyboardButton(text=r'\ ', callback_data='INGAME: down-right')
move_up = types.InlineKeyboardButton(text='⬆️', callback_data='INGAME: up')
menu = types.InlineKeyboardButton(text="M", callback_data='INGAME: menu')
up_left = types.InlineKeyboardButton(text=r'\ ', callback_data='INGAME: up-left')
up_right = types.InlineKeyboardButton(text='/', callback_data='INGAME: up-right')
move_left = types.InlineKeyboardButton(text='⬅️', callback_data='INGAME: left')
move_right = types.InlineKeyboardButton(text='➡️', callback_data='INGAME: right')


def update_change(message, language):
    uid = message.from_user.id

    print(f"--//TASK: Request {uid}")
    kb = types.InlineKeyboardMarkup()
    menu.text = localization.menu_text.get(language)
    kb.add(up_left, move_up, up_right, move_left, menu, move_right, down_left, move_down, down_right)
    msgID = messageManagment.return_latest_messageID(message, uid=uid)

    while shm.buf[int(str(uid)[-3:])] == 0:
        pass

    if shm.buf[int(str(uid)[-3:])] == 2:
        return

    if shm.buf[int(str(uid)[-3:])] == 1:
        with open(f'./generated/{uid}.png', 'rb') as f:
            media = telebot.types.InputMediaPhoto(f.read())

        try:
            bot.edit_message_media(chat_id=uid, message_id=msgID, media=media, reply_markup=kb)
        except telebot.apihelper.ApiTelegramException:
            pass

        user = ReadAndWrite(uid)
        debug = user.read('debug')

        if debug == 'True':
            current_slot = user.read('current_slot')
            pos = user.read('pos', current_slot)
            name = user.read('name', current_slot)
            cmap = user.read('map', current_slot)
            value = user.read('???_value', current_slot)
            status = user.read('status', current_slot)

            caption = f'{pos}, Facing={status}\nLanguage={language}, Debug={debug}, Current_SaveSlot={current_slot}, Slot_Name = {name}, Value = {value}, map = {cmap}\n uid={message.from_user.id}, latest_messageID={msgID}'
            try:
                bot.edit_message_caption(chat_id=uid, message_id=msgID, caption=caption, reply_markup=kb)
            except telebot.apihelper.ApiTelegramException:
                pass

        shm.buf[int(str(uid)[-3:])] = 0
