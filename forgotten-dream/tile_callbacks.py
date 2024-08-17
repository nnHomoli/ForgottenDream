import telebot
import messageManagment
import localization
import misc
import update
from userDataManagment import ReadAndWrite
from telebot import types
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


def client_callback(message, call, language, pos):
    msgID = messageManagment.return_latest_messageID(message)
    user = ReadAndWrite(message.from_user.id)
    slot = user.read('current_slot')

    initial_direction = user.read('direction', slot)
    direction = misc.calculate_direction(pos)

    entity_check = user.get_sprite_properties("entity", call,"call", slot)
    if entity_check is not None:
        misc.entity_direction_to_player(call, message.from_user.id)
    if initial_direction != direction:
        user.ChangeValue('direction', direction, slot)

    if initial_direction != direction or entity_check is not None:
        update.update_change(message, language)

    kb = types.InlineKeyboardMarkup()

    caption = ''

    skipDialogue = types.InlineKeyboardButton(text=localization.next_dialogue.get(language),
                                              callback_data='DIALOGUE: skipDialogue')

    if call == '1509_generalcallback':
        Dialogue = "This is <strong>someone's</strong> house... <strong>Someone</strong> lives there..." if language == 'English' else "Это дом <strong>кого-то</strong>... <strong>Кто-то</strong> живет там..."

        misc.change_dialogue_text(message, Dialogue)

        kb.add(skipDialogue)
        bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, reply_markup=kb)
        
    elif call == "1002_generalcallback":
        Dialogue = "Stairs... that leads to <strong>somewhere</strong>..." if language == 'English' else ("Ступени... "
                                                                                                          "которые "
                                                                                                          "идут "
                                                                                                          "<strong>куда-то</strong>...")
        caption = "<em>You're not feeling like going there...</em>" if language == 'English' else ("<em>Ты не "
                                                                                                   "чувствуешь особой"
                                                                                                   " нужды идти "
                                                                                                   "туда...</em>")

        misc.change_dialogue_text(message, Dialogue)

        kb.add(skipDialogue)
        bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, reply_markup=kb,
                                 parse_mode='HTML')

    elif call == '222_generalcallback':
        Dialogue = "The door is closed... <strong>but not locked</strong>..." if language == 'English' else ("Дверь "
                                                                                                             "закрыта... <strong>но не замкнута</strong>...")
        caption = "Do you want to <em>open it</em>?" if language == 'English' else "Хочешь ли ты её <em>открыть</em>?"

        misc.change_dialogue_text(message, Dialogue)

        Yes = types.InlineKeyboardButton(text=localization.yes_generic.get(language), callback_data='DIALOGUE: 222_Yes')
        No = types.InlineKeyboardButton(text=localization.no_generic.get(language), callback_data='DIALOGUE: skipDialogue')

        kb.add(No, Yes)
        bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, reply_markup=kb,
                                 parse_mode='HTML')

    elif call == "1124_generalcallback" or call == "1125_generalcallback":
        Dialogue = "hmm... looks like there's nothing <strong>really special</strong>..." if language == 'English' else "Хм... похоже тут нет ничего <strong>очень особенного</strong>..."
        caption = "Do you want to <em>leave</em>?" if language == 'English' else "Хочешь ли ты <em>выйти</em>?"

        misc.change_dialogue_text(message, Dialogue)

        Yes = types.InlineKeyboardButton(text=localization.yes_generic.get(language), callback_data='DIALOGUE: 1124x5_Yes')
        No = types.InlineKeyboardButton(text=localization.no_generic.get(language), callback_data='DIALOGUE: skipDialogue')

        kb.add(No, Yes)
        bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, reply_markup=kb,
                                 parse_mode='HTML')

    elif call == "210_generalcallback":
        Dialogue = "Table... <em>just a table...</em>" if language == 'English' else "Стол... <em>просто стол...</em>"

        misc.change_dialogue_text(message, Dialogue)

        kb.add(skipDialogue)
        bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, reply_markup=kb,
                                 parse_mode='HTML')

    elif call == "211_generalcallback" or call == "209_generalcallback":
        Dialogue = "<strong>Stool...</strong>" if language == 'English' else "<strong>Стул...</strong>"

        misc.change_dialogue_text(message, Dialogue)

        kb.add(skipDialogue)
        bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, reply_markup=kb,
                                 parse_mode='HTML')

    elif call == "1573_generalcallback" or call == "1572_generalcallback":
        value = user.read('???_value', slot)
        inventory = user.read('inventory', slot)

        Dialogue = "<em>Bush</em>" if language == 'English' else "<em>Куст</em>"

        if value > 6 and (inventory is None or 'Leaf' not in [item for item, count in inventory]):
            Dialogue = "Bush...<em>Strange bush...</em>" if language == 'English' else "Куст...<em>Странный куст...</em>"
            getItem = types.InlineKeyboardButton(text=localization.next_dialogue.get(language),
                                                 callback_data='DIALOGUE: TILE1573x72_get_???')

            kb.add(getItem)

        else:
            kb.add(skipDialogue)

        misc.change_dialogue_text(message, Dialogue)

        bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, reply_markup=kb,
                                 parse_mode='HTML')

    elif call == "369_generalcallback" or call == "305_generalcallback":
        Dialogue = "<strong>Tree</strong>" if language == 'English' else "<strong>Дерево</strong>"

        misc.change_dialogue_text(message, Dialogue)

        kb.add(skipDialogue)
        bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, reply_markup=kb,
                                 parse_mode='HTML')

    elif call == "277_generalcallback" or call == "278_generalcallback":
        Dialogue = "Bench, <em>What is it doing here?</em>" if language == 'English' else "Скамейка, <em>Что она тут делает?</em>"

        misc.change_dialogue_text(message, Dialogue)

        kb.add(skipDialogue)
        bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, reply_markup=kb,
                                 parse_mode='HTML')

    elif call == "1314_generalcallback" or call == "1250_generalcallback":
        Dialogue = "Plant" if language == 'English' else "Растение"

        misc.change_dialogue_text(message, Dialogue)

        kb.add(skipDialogue)
        bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, reply_markup=kb,
                                 parse_mode='HTML')

    elif call == "1258_generalcallback" or call == "1194_generalcallback":
        Dialogue = "Questionable shelf" if language == 'English' else "Вопросительный шкаф"

        misc.change_dialogue_text(message, Dialogue)

        kb.add(skipDialogue)
        bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, reply_markup=kb,
                                 parse_mode='HTML')

    elif call == "1004_generalcallback":
        Dialogue = "<em>There's writing on a table</em>" if language == 'English' else "<em>Записка на столе</em>"
        caption = "It has very bad writing, you can't read it..." if language == 'English' else "Она имеет очень плохой подчерк, ты не можешь её прочитать..."

        misc.change_dialogue_text(message, Dialogue)

        kb.add(skipDialogue)
        bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, reply_markup=kb,
                                 parse_mode='HTML')

    elif call == "854_generalcallback":
        user.read('personal_sprites', slot)

    elif call == "test_room_teleport":
        user.ChangeValue('map', 'testroomFirst', slot)
        user.ChangeValue('pos', (528, 432), slot)
        user.ChangeValue('direction', 'left', slot)

        update.update_change(message, language)

    elif call == "197_generalcallback":
        user.ChangeValue('map', 'screenburninExtended', slot)
        user.ChangeValue('pos', (448, 448), slot)
        user.ChangeValue('direction', 'left', slot)

        update.update_change(message, language)

    elif call == 'party_character':
        user.delete_sprite('entity', 'party_character', slot)

        caption = "[][][][] has joined the party!" if language == 'English' else "[][][][] присоединяется к группе!"

        following_character = ('following_test_character', (256, 480), 'down', (12, 76, 140, 204))
        user.AppendValue('party', following_character, slot)

        kb.add(skipDialogue)
        bot.edit_message_caption(chat_id=message.from_user.id, message_id=msgID, caption=caption, reply_markup=kb,
                                 parse_mode='HTML')
