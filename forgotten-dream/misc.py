import telebot
import messageManagment
from config import TOKEN
from userDataManagment import ReadAndWrite

bot = telebot.TeleBot(TOKEN)


def retrieve_profile_name(message, slot):
    try:
        slot_Name = ReadAndWrite(message.from_user.id).read('name', slot)

    except Exception:
        slot_Name = 'None'

    return slot_Name


def dialogue_box(message):
    box = ['|']

    for item in box:
        dialogue_ID = bot.send_message(message.from_user.id, item)

        messageManagment.write_messageID(message, dialogue_ID)


def get_shm_name():
    with open('./shm_cache.txt', 'r') as r:
        lines = r.readlines()
    return lines[-1]


def change_dialogue_text(message, text=None):
    try:
        with open(f'./chatIDmessageID/{message.from_user.id}.txt', 'r') as latest:
            lines = latest.readlines()
            middle_box = lines[0]

        if text is not None:
            text = '| ' + text

        else:
            text = '|'

        bot.edit_message_text(chat_id=message.from_user.id, message_id=middle_box, text=text, parse_mode='HTML')
    except telebot.apihelper.ApiTelegramException:
        pass


def entity_direction_to_player(entity_callback, uid):
    user = ReadAndWrite(uid)
    slot = user.read('current_slot')
    player_pos = user.read('pos', slot)
    unit_pos = user.get_sprite_properties("entity", entity_callback, "pos", slot)
    final_direction = {
        player_pos[0] < unit_pos[0]: 'left',
        player_pos[0] > unit_pos[0]: 'right',
        player_pos[1] > unit_pos[1]: 'down',
        player_pos[1] < unit_pos[1]: 'up'
    }

    user.change_sprite_properties("entity", entity_callback, "direction", final_direction[True], slot)


def calculate_direction(pos):
    direction = {
        pos[0] < 0: 'left',
        pos[0] > 0: 'right',
        pos[1] > 0: 'down',
        pos[1] < 0: 'up'
    }

    return direction.get(True)
