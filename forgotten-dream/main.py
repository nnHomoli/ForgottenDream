import pygame
import os
import sys
import queue
import time
import threading
import subprocess
from level import Level
from timeout import timeout
from multiprocessing import shared_memory
from config import display_resolution, gen_path
from userDataManagment import ReadAndWrite
from PIL import Image, ImageFilter, ImageEnhance


class GameServer:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('ForgottenDream')
        pygame.display.set_icon(pygame.image.load('./mapdev/icon.ico'))

        self.screen = pygame.display.set_mode(display_resolution, pygame.SRCALPHA)
        pygame.display.iconify()

        self.maps = {}

        for map_dir in os.listdir('./maps'):
            if os.path.isdir(f'./maps/{map_dir}') and map_dir != 'colliders':
                self.maps.update({map_dir: Level(map_dir)})

        self.shm = shared_memory.SharedMemory(create=True, size=999)
        with open('./shm_cache.txt', 'w') as w:
            w.write(str(self.shm.name))

        self.bot = subprocess.Popen(["python", 'secondary.py'],shell=(True if os.name == "nt" else False),
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        self.tasks = queue.Queue()
        self.ServerLoop()

    def ServerLoop(self):
        threading.Thread(target=self.Listening).start()
        repeat = True

        while True:
            if repeat:
                print("--//SERVER: Listening...")
                repeat = False

            if pygame.event.get(pygame.QUIT):
                os.remove("./shm_cache.txt")
                pygame.quit()

            if not self.tasks.empty():
                task = self.tasks.get()
                if "Request " in task:
                    print("--//SERVER: Received...")
                    pygame.event.get()
                    repeat = True

                    uid = task.replace('Request ', '')
                    self.imageRender(uid)

    def imageRender(self, uid):
        print("--//SERVER: Rendering...\n")
        time_start = time.perf_counter()
        try:
            self.render(uid)
        except TimeoutError:
            self.shm.buf[int(uid[-3:])] = 2
            raise Warning("--//SERVER: Render Timeout at " + uid)

        self.shm.buf[int(uid[-3:])] = 1

        print(f"--//SERVER: Finished {uid} in {time.perf_counter() - time_start:0.4F} seconds")

    @timeout(3)
    def render(self, uid):
        user = ReadAndWrite(uid)
        slot = user.read('current_slot')
        location = user.read('map', slot)
        if location in self.maps:
            Lmap = self.maps.get(location)
            Lmap.render_player(uid)
            try:
                img_path = f'{gen_path}/{uid}.png'
                pygame.image.save(self.screen, img_path)
                ImageEnhance.Contrast(Image.open(img_path).filter(ImageFilter.SHARPEN)).enhance(0.95).save(img_path)

            except pygame.error as e:
                raise Warning(e)

    def Listening(self):
        while True:
            line = self.bot.stdout.readline().decode("utf-8").replace('\n', '').replace('\r', '')
            if line:
                print(line)
                if "--//TASK:" in line:
                    self.tasks.put(line.replace('--//TASK: ', ''))


if __name__ == '__main__':
    GameServer()
