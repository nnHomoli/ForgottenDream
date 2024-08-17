import telebot
import localization
import messageManagment
import misc
import player_update
from telebot import types
from userDataManagment import ReadAndWrite
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


def add_to_inventory(message, item, count, stack='no', notification='no'):
    user = ReadAndWrite(message.from_user.id)
    current_slot = user.read('current_slot')
    language = user.read('language')

    inventory = user.GetValues('inventory', current_slot)

    if inventory is None or not any(item == item_data[0] for item_data in inventory):
        user.AppendValue('inventory', (item, count), current_slot)

        if stack == 'no' and notification == 'yes':
            item_notification(message, item, language)

    elif stack == 'yes' and inventory is not None:
        for i, item_data in enumerate(inventory):
            if item_data[0] == item:
                name, inv_count = item_data
                inventory[i] = (name, count + inv_count)
                user.ChangeValue('inventory', inventory, current_slot)

                if notification == 'yes':
                    item_notification(message, item, language)

    else:
        misc.change_dialogue_text(message)
        player_update.move_player(message, (0, 0))


def item_notification(message, item, language):
    kb = types.InlineKeyboardMarkup()
    msgID = messageManagment.return_latest_messageID(message)

    Skip = types.InlineKeyboardButton(text=localization.next_dialogue.get(language), callback_data='DIALOGUE: skipDialogue')

    name = localization.items.get(f'{item}_{language}')
    caption = f'You got <em>{name}</em>!' if language == 'English' else f'Вы получили <em>{name}</em>!'

    kb.add(Skip)
    bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, reply_markup=kb,
                             parse_mode='HTML')
