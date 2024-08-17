import telebot
import menu
import update
import tile_callbacks
from userDataManagment import ReadAndWrite
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


def move_player(message, pos):
    user = ReadAndWrite(message.from_user.id)
    menu_status = user.read('menu')
    language = user.read('language')

    if menu_status == 'menu_off':
        x2 = user.read('x2_mode')

        output = user.MovePlayerPosBy(pos)
        if x2 == 'True':
            output = user.MovePlayerPosBy(pos)
            update.update_change(message, language)

        if output is not None:
            tile_callbacks.client_callback(message, output, language, pos)

        else:
            update.update_change(message, language)

    else:
        menu.menu(message, menu_status, language)
