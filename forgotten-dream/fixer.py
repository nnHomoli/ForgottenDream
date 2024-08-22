import os
import threading

import messageManagment
from config import chat_path, gen_path
from datetime import datetime, timedelta

class Fixers:
    def __init__(self):
        self.at_work = []
        self.functions = [self.__message_fixer, self.__data_assistant]
        self.kill = False

    def __message_fixer(self):
        while not self.kill:
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
                            messageManagment.delete_old_messages(uid=uid)
                except FileNotFoundError:
                    pass

    def __data_assistant(self):
        while not self.kill:
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

    def exit(self):
        self.kill = True
        for thread in self.at_work:
            thread.join()

    def start(self):
        for func in self.functions:
            func_thread = threading.Thread(target=func)
            func_thread.daemon = True
            func_thread.start()
            self.at_work.append(func_thread)

