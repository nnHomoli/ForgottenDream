import os
import misc
import menu
import telebot
import dialogue
import inventory
import localization
import player_update
import profileManagment
import messageManagment
from config import TOKEN
from telebot import types
from userDataManagment import ReadAndWrite

bot = telebot.TeleBot(TOKEN)

movement = {
    "down": (0, 16),
    "up": (0, -16),
    "right": (16, 0),
    "left": (-16, 0),

    "down-left": (-16, 16),
    "up-left": (-16, -16),
    "down-right": (16, 16),
    "up-right": (16, -16)
}


def INGAME(call):
    out = call.data.replace("INGAME: ", "")
    if out != "menu":
        player_update.move_player(call, movement.get(out))

    else:
        user = ReadAndWrite(call.from_user.id)
        last = user.read('menu')
        user.ChangeValue('last_menu', last)
        user.ChangeValue('menu', 'menu_on')

        player_update.move_player(call, (0, 0))


def DIALOGUE(call):
    out = call.data.replace("DIALOGUE: ", "")
    if out == 'skipDialogue':
        misc.change_dialogue_text(call)
        player_update.move_player(call, (0, 0))

    elif out == 'TILE1573x72_get_???':
        inventory.add_to_inventory(call, 'Leaf', 1, notification='yes')

    elif out == "222_Yes":
        misc.change_dialogue_text(call)
        user = ReadAndWrite(call.from_user.id)

        slot = user.read('current_slot')
        user.ChangeValue('map', 'screenburninHouse', slot)
        user.ChangeValue('pos', (368, 320), slot)
        user.ChangeValue('direction', 'down', slot)

        player_update.move_player(call, (0, 0))

    elif out == '1124x5_Yes':
        misc.change_dialogue_text(call)

        user = ReadAndWrite(call.from_user.id)

        slot = user.read('current_slot')
        user.ChangeValue('map', 'screenburninExtended', slot)
        user.ChangeValue('pos', (192, 512), slot)
        user.ChangeValue('direction', 'down', slot)

        player_update.move_player(call, (0, 0))


def SYSTEM(call):
    out = call.data.replace("SYSTEM: ", "")
    if out == 'update':
        player_update.move_player(call, (0, 0))

    elif out.startswith('inventoryItem'):
        user = ReadAndWrite(call.from_user.id)
        language = user.read('language')

        dialogue_text = dialogue.inventory.get(f"{language}_{out.replace('inventoryItem ', '')}")

        misc.change_dialogue_text(call, dialogue_text)

    elif out == "inventory":
        user = ReadAndWrite(call.from_user.id)
        last = user.read('menu')
        user.ChangeValue('last_menu', last)

        user.ChangeValue('menu', 'inventory')

        player_update.move_player(call, (0, 0))

    elif out == 'slotDeletion':
        menu.slot_deletion(call)

    elif out.startswith('slotDelete'):
        profileManagment.delete_slot(call, out.replace('slotDelete ', ''))

    elif out == 'SaveMenu':
        user = ReadAndWrite(call.from_user.id)
        last = user.read('menu')
        user.ChangeValue('last_menu', last)

        user.ChangeValue('menu', 'Save_Menu')

        player_update.move_player(call, (0, 0))

    elif out.startswith('slotExisting'):
        profileManagment.change_slot(call, out.replace('slotExisting ', ''))

    elif out == 'Resume':
        userD = ReadAndWrite(call.from_user.id)
        userD.ChangeValue('menu', 'menu_off')

        player_update.move_player(call, (0, 0))

    elif out == 'change_to_english':
        UserD = ReadAndWrite(call.from_user.id)
        UserD.ChangeValue('language', 'English')

        player_update.move_player(call, (0, 0))

    elif out == 'change_to_russian':
        UserD = ReadAndWrite(call.from_user.id)
        UserD.ChangeValue('language', 'Russian')

        player_update.move_player(call, (0, 0))

    elif out == 'BackToLastMenu':
        misc.change_dialogue_text(call)
        user = ReadAndWrite(call.from_user.id)
        lastMenu = user.read('last_menu')
        current_slot = user.read('current_slot')

        if current_slot is not None and lastMenu is not None:
            user.ChangeValue('menu', f'{lastMenu}')

        else:
            user.ChangeValue('menu', 'menu_start_on')

        player_update.move_player(call, (0, 0))

    elif out == 'ToggleDebug':
        user = ReadAndWrite(call.from_user.id)
        debugCheck = user.read('debug')

        toggle = debugCheck == 'False'

        user.ChangeValue('debug', str(toggle))
        player_update.move_player(call, (0, 0))

    elif out == 'DeleteData':
        msgID = messageManagment.return_latest_messageID(call)
        user = ReadAndWrite(call.from_user.id)
        language = user.read('language')

        kb = types.InlineKeyboardMarkup()

        caption = 'Are you sure you want to <strong>delete ALL</strong> your data?' if language == 'English' else 'Вы уверены, что хотите <strong>удалить ВСЕ</strong> свои данные?'

        Sure = types.InlineKeyboardButton(text=localization.sure.get(language), callback_data='SYSTEM: DeleteDataSure')
        NotSure = types.InlineKeyboardButton(text=localization.notsure.get(language), callback_data='SYSTEM: DeleteDataNotSure')

        kb.add(NotSure, Sure)

        bot.edit_message_caption(chat_id=call.from_user.id, message_id=msgID, caption=caption, reply_markup=kb,
                                 parse_mode='HTML')

    elif out == 'DeleteDataNotSure':
        player_update.move_player(call, (0, 0))

    elif out == 'DeleteDataSure':
        try:
            os.remove(f'./thegameuserdata/[{call.from_user.id}].json')
            os.remove(f'./generated/{call.from_user.id}.png')

        except os.error:
            pass

        slots = {
            1: f'./thegameuserdata/[{call.from_user.id}_1].json',
            2: f'./thegameuserdata/[{call.from_user.id}_2].json',
            3: f'./thegameuserdata/[{call.from_user.id}_3].json'
        }

        for slot in slots:
            if os.path.exists(slots[slot]):
                os.remove(slots[slot])

        messageManagment.delete_old_messages(call)
        os.remove(f'./chatIDmessageID/{call.from_user.id}.txt')

    elif out == 'Settings':
        user = ReadAndWrite(call.from_user.id)
        last = user.read('menu')
        user.ChangeValue('last_menu', last)

        user.ChangeValue('menu', 'Settings')

        player_update.move_player(call, (0, 0))

    elif out == 'MainMenu':
        UserD = ReadAndWrite(call.from_user.id)
        UserD.ChangeValue('menu', 'menu_start_on')

        player_update.move_player(call, (0, 0))

    elif out == 'ToggleX2':
        user = ReadAndWrite(call.from_user.id)
        value = user.read('x2_mode')

        toggle = value == 'False'

        user.ChangeValue('x2_mode', str(toggle))
        player_update.move_player(call, (0, 0))

    elif out == 'Continue':
        userD = ReadAndWrite(call.from_user.id)
        userD.ChangeValue('menu', 'menu_off')

        player_update.move_player(call, (0, 0))
