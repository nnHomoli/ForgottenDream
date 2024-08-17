import re
import os
import time
import telebot
import player_update
import messageManagment
from userDataManagment import ReadAndWrite
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


def create_new_slot_p2(message, slot, lang, msgID, start, create_new_slot):
    slot_Name = message.text

    if re.match(r'^[a-zA-Z]+$', slot_Name) and len(slot_Name) <= 25:
        userD = ReadAndWrite(message.from_user.id)
        userD.register_slot(slot, slot_Name)
        userD.ChangeValue('current_slot', str(slot))
        userD.ChangeValue('menu', 'menu_off')
        q_value_q = userD.read('???_value', slot)

        if q_value_q > 1:
            tile_for_test_room = (
            'test_room_teleport', (464, 448), 'events', 'screenburninExtended', 'visible', 197, 'True')
            party_character = (
            'party_character', (256, 480), None, 'down', 'testroomFirst', 'visible', (12, 76, 140, 204), 'standby')

            userD.AppendValue('personal_sprites', tile_for_test_room, slot)
            userD.AppendValue('personal_entities', party_character, slot)

        caption = f'Successfully created a new Character...\n\n Welcome to this world, <em>{slot_Name}</em>!' if lang == 'English' else f'Успешно создан новый Персонаж...\n\n Добро пожаловать в этот мир, <em>{slot_Name}</em>!'

        bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, parse_mode='HTML')

        time.sleep(5)

        start(message)

    else:
        caption = 'Invalid name, please check that name <strong>contains english letters only</strong> and <strong>is not longer than 25 characters</strong>\n     | Please, wait 10 seconds |' if lang == 'English' else 'Неверное имя, пожалуйста, проверьте, что имя содержит <strong>только английские буквы</strong> <strong>и не превышает 25 символов</strong>\n     | Пожалуйста, подождите 10 секунд |'

        bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, parse_mode='HTML')
        time.sleep(10)

        create_new_slot(message, slot, loop=True)


def delete_slot(message, slot):
    msgID = messageManagment.return_latest_messageID(message)

    user = ReadAndWrite(message.from_user.id)

    current_slot = user.read('current_slot')
    slot_name = user.read('name', slot)
    language = user.read('language')

    if current_slot is not None and int(current_slot) == int(slot):
        user.ChangeValue('current_slot', None)

    filepath = f'./thegameuserdata/[{message.from_user.id}_{slot}].json'

    if os.path.exists(filepath):
        os.remove(filepath)

        caption = f"...And just like that...\n\n                        ...<em>{slot_name}</em> has <strong>succumbed</strong>..." if language == 'English' else f"...И просто так легко...\n\n                          ...{slot_name} <strong>сдался</strong>..."

        bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, parse_mode='HTML')

        time.sleep(5)

    player_update.move_player(message, (0, 0))


def change_slot(message, slot):
    userD = ReadAndWrite(message.from_user.id)
    userD.ChangeValue('current_slot', f'{slot}')
    userD.ChangeValue('menu', 'menu_off')

    player_update.move_player(message, (0, 0))
