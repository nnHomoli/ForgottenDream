import telebot
import localization
import messageManagment
import misc
from telebot import types
from pathlib import Path
from userDataManagment import ReadAndWrite
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


def menu(message, typeOf, language):
    msgID = messageManagment.return_latest_messageID(message)
    kb = types.InlineKeyboardMarkup()
    back_to_last_menu = types.InlineKeyboardButton(text=localization.back.get(language),
                                                   callback_data='SYSTEM: BackToLastMenu')
    user = ReadAndWrite(message.from_user.id)

    if typeOf == 'menu_on':

        caption = '**%forgotten dream%**\n\n<strong>PAUSE MENU</strong>⏸️:\n~~~~~~~~~~~~~~~~~~~|\n\n' if language == 'English' else '**%forgotten dream%**\n\n<strong>МЕНЮ ПАУЗЫ</strong>⏸️:\n~~~~~~~~~~~~~~~~~~~|\n\n'

        Resume = types.InlineKeyboardButton(text=localization.Resume.get(language), callback_data='SYSTEM: Resume')
        Settings = types.InlineKeyboardButton(text=localization.Settings.get(language),
                                              callback_data='SYSTEM: Settings')
        SaveMenu = types.InlineKeyboardButton(text=localization.SaveMenu.get(language),
                                              callback_data='SYSTEM: SaveMenu')
        inventory = types.InlineKeyboardButton(text=localization.inventory.get(language),
                                               callback_data='SYSTEM: inventory')

        kb.row(Resume)
        kb.row(inventory, SaveMenu)
        kb.row(Settings)

        slot = user.read('current_slot')
        current_map = user.read('map', slot)

        with open(f'./maps/{current_map}/fullmap.png', 'rb') as f:
            photo = telebot.types.InputMediaPhoto(f.read())

        bot.edit_message_media(media=photo, chat_id=message.from_user.id, message_id=msgID)

    elif typeOf == 'inventory':
        current_slot = user.read('current_slot')

        caption = "Inventory:\n~~~~~~~~~~~~~~~~~~~|\n\n" if language == 'English' else ("Инвентарь:\n"
                                                                                        "~~~~~~~~~~~~~~~~~~~|\n\n")

        inventory = user.GetValues('inventory', current_slot)
        if inventory is not None:
            for item in inventory:
                name, count = item
                name_localization = localization.items.get(f'{name}_{language}')
                kb.add(
                    types.InlineKeyboardButton(text=f'{name_localization} x{count}',
                                               callback_data=f'SYSTEM: inventoryItem {name}'))

        kb.add(back_to_last_menu)

    elif typeOf == 'Settings':
        Debug = user.read('debug')
        x2_mode = user.read('x2_mode')

        lang_out = localization.localization.get(language)
        debug_out = localization.falsetrue.get(f'{language}_{Debug}')
        x2_out = localization.falsetrue.get(f'{language}_{x2_mode}')

        caption = f'<strong>SETTINGS</strong>:\n~~~~~~~~~~~~~~~~~~~|\n    'r'/\ 'f'\n        The current Language is: {lang_out}\n\
        Debug Mode is: {debug_out}\n\
        x2 Movement Speed is: {x2_out}\n\
    'r'\/'' \n\n\n' if language == "English" else \
            f'<strong>Настройки</strong>:\n~~~~~~~~~~~~~~~~~~~|\n    'r'/\ 'f'\n\
        Текущий язык: {lang_out}\n        Режим отладки: {debug_out}\n\
        x2 Скорость Передвижения: {x2_out}\n    'r'\/'' \n\n\n'

        DeleteData = types.InlineKeyboardButton(text=localization.deleteData.get(language),
                                                callback_data='SYSTEM: DeleteData')
        changeLanguage = types.InlineKeyboardButton(text=localization.change_language.get(language),
                                                    callback_data="SYSTEM: " + localization.change_which.get(language))
        ToggleDebug = types.InlineKeyboardButton(text=localization.debug.get(language),
                                                 callback_data='SYSTEM: ToggleDebug')
        ToggleX2 = types.InlineKeyboardButton(text=localization.x2_toggle.get(language),
                                              callback_data='SYSTEM: ToggleX2')

        kb.row(changeLanguage)
        kb.row(ToggleDebug)
        kb.row(ToggleX2)
        kb.row(DeleteData)
        kb.row(back_to_last_menu)

    elif typeOf == 'Save_Menu':
        SlotNumber1 = Path(f'./thegameuserdata/[{message.from_user.id}_1].json')
        SlotNumber2 = Path(f'./thegameuserdata/[{message.from_user.id}_2].json')
        SlotNumber3 = Path(f'./thegameuserdata/[{message.from_user.id}_3].json')

        SlotNumber1_name = misc.retrieve_profile_name(message, 1)
        SlotNumber2_name = misc.retrieve_profile_name(message, 2)
        SlotNumber3_name = misc.retrieve_profile_name(message, 3)

        if language == 'English':
            slot_buttons = {
                SlotNumber1: {'text': f'First slot -- {SlotNumber1_name}', 'cback_data': 'SYSTEM: slotExisting 1',
                              'textEmpty': 'Empty slot', 'cback_data_empty': 'SYSTEM: slotEMPTY 1'},
                SlotNumber2: {'text': f'Second slot -- {SlotNumber2_name}', 'cback_data': 'SYSTEM: slotExisting 2',
                              'textEmpty': 'Empty slot', 'cback_data_empty': 'SYSTEM: slotEMPTY 2'},
                SlotNumber3: {'text': f'Third slot -- {SlotNumber3_name}', 'cback_data': 'SYSTEM: slotExisting 3',
                              'textEmpty': 'Empty slot', 'cback_data_empty': 'SYSTEM: slotEMPTY 3'}
            }

        elif language == 'Russian':
            slot_buttons = {
                SlotNumber1: {'text': f'Первый слот -- {SlotNumber1_name}', 'cback_data': 'SYSTEM: slotExisting 1',
                              'textEmpty': 'Пустой слот', 'cback_data_empty': 'SYSTEM: slotEMPTY 1'},
                SlotNumber2: {'text': f'Второй слот -- {SlotNumber2_name}', 'cback_data': 'SYSTEM: slotExisting 2',
                              'textEmpty': 'Пустой слот', 'cback_data_empty': 'SYSTEM: slotEMPTY 2'},
                SlotNumber3: {'text': f'Третий слот -- {SlotNumber3_name}', 'cback_data': 'SYSTEM: slotExisting 3',
                              'textEmpty': 'Пустой слот', 'cback_data_empty': 'SYSTEM: slotEMPTY 3'}
            }

        captionFull = (
            f'<strong>Character Slots</strong>:\n~~~~~~~~~~~~~~~~~~~|\n    'r'/\ ''\n      Choose slot to load '
            f'character\n      or delete slot to create a new one\n    'r'\/'' \n\n\n') if (language ==
                                                                                            "English") else \
            (f'<strong>Слоты персонажей</strong>:\n~~~~~~~~~~~~~~~~~~~|\n    'r'/\ ''\n      Выберите слот для загрузки '
             f'персонажа\n      или удалите слот для создания нового\n    'r'\/'' \n\n\n')
        captionEmpty = (
            f'<strong>Character Slots</strong>:\n~~~~~~~~~~~~~~~~~~~|\n    'r'/\ ''\n      Choose empty slot to '
            f'create\n      a new character\n    'r'\/'' \n\n\n') if language == "English" else \
            (f'<strong>Слоты персонажей</strong>\n~~~~~~~~~~~~~~~~~~~|\n    'r'/\ ''\n      Выберите пустой слот,'
             '\n      чтобы создать нового персонажа\n    'r'\/'' \n\n\n')

        deleteSlot = types.InlineKeyboardButton(text=localization.delete_slot.get(language),
                                                callback_data='SYSTEM: slotDeletion')

        caption = captionFull
        for slot_button, data in slot_buttons.items():
            if slot_button.exists():
                kb.add(types.InlineKeyboardButton(text=data['text'], callback_data=data['cback_data']))

            if not slot_button.exists():
                caption = captionEmpty
                kb.add(types.InlineKeyboardButton(text=data['textEmpty'], callback_data=data['cback_data_empty']))

        kb.row(deleteSlot)
        kb.row(back_to_last_menu)

    elif typeOf == 'menu_start_on':
        Continue = types.InlineKeyboardButton(text=localization.continuwe.get(language),
                                              callback_data='SYSTEM: SaveMenu')
        Settings = types.InlineKeyboardButton(text=localization.settings.get(language),
                                              callback_data='SYSTEM: Settings')

        caption = '**%Forgotten Dream%**\n\n<strong>START MENU</strong>⏸️:\n~~~~~~~~~~~~~~~~~~~|\n\n' if (language ==
                                                                                                          'English') else \
            '**%Forgotten Dream%**\n\n<strong>СТАРТ МЕНЮ</strong>⏸️:\n~~~~~~~~~~~~~~~~~~~|\n\n'

        kb.row(Continue)
        kb.row(Settings)

        with open('./mapdev/mapFull.png', 'rb') as f:
            photo = telebot.types.InputMediaPhoto(f.read())

        bot.edit_message_media(media=photo, chat_id=message.from_user.id, message_id=msgID)

    bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, reply_markup=kb,
                             parse_mode='HTML')


def slot_deletion(message):
    msgID = messageManagment.return_latest_messageID(message)
    kb = types.InlineKeyboardMarkup()

    user = ReadAndWrite(message.from_user.id)
    language = user.read('language')

    SlotNumber1 = Path(f'./thegameuserdata/[{message.from_user.id}_1].json')
    SlotNumber2 = Path(f'./thegameuserdata/[{message.from_user.id}_2].json')
    SlotNumber3 = Path(f'./thegameuserdata/[{message.from_user.id}_3].json')

    SlotNumber3_name = misc.retrieve_profile_name(message, 3)
    SlotNumber2_name = misc.retrieve_profile_name(message, 2)
    SlotNumber1_name = misc.retrieve_profile_name(message, 1)

    if language == 'English':

        slot_buttons = {
            SlotNumber1: {'text': f'First slot -- {SlotNumber1_name}', 'cback_data': 'SYSTEM: slotDelete 1'},
            SlotNumber2: {'text': f'Second slot -- {SlotNumber2_name}', 'cback_data': 'SYSTEM: slotDelete 2'},
            SlotNumber3: {'text': f'Third slot -- {SlotNumber3_name}', 'cback_data': 'SYSTEM: slotDelete 3'}
        }

    elif language == 'Russian':

        slot_buttons = {
            SlotNumber1: {'text': f'Первый слот -- {SlotNumber1_name}', 'cback_data': 'SYSTEM: slotDelete 1'},
            SlotNumber2: {'text': f'Второй слот -- {SlotNumber2_name}', 'cback_data': 'SYSTEM: slotDelete 2'},
            SlotNumber3: {'text': f'Третий слот -- {SlotNumber3_name}', 'cback_data': 'SYSTEM: slotDelete 3'}
        }

    back = types.InlineKeyboardButton(text=localization.back.get(language), callback_data='SYSTEM: update')

    caption = ("<strong>You will not be able to go back after deletion</strong>\n\n...If you want to continue...\n\n   "
               "                      ...Choose <em>slot</em> to delete...") if language == "English" else \
        ("<strong>Вы не сможете вернуться назад после удаления</strong>\n\n...Если вы уверены в своём выборе...\n\n    "
         "           ...Выберите <em>слот</em> для удаления...")

    for slot_button, data in slot_buttons.items():
        if slot_button.exists():
            kb.add(types.InlineKeyboardButton(text=data['text'], callback_data=data['cback_data']))

    kb.add(back)

    bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, reply_markup=kb,
                             parse_mode='HTML')
