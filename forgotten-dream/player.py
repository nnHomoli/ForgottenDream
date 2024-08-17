import pygame
import random
from tilesetreader import tilesetRead
from userDataManagment import ReadAndWrite


class Player(pygame.sprite.Sprite):

    def __init__(self, udata, groups):
        super().__init__(groups)
        self.tileset = tilesetRead('./mapdev/tileset/p.tsx')

        user = ReadAndWrite(udata)

        self.slot = user.read('current_slot')
        self.pos = user.read("pos", self.slot)
        self.animation = user.read("animation", self.slot)
        if self.animation is None:
            self.direction = user.read("direction", self.slot)

            direction = {
                'down': random.randint(0, 1),
                'up': random.randint(2, 3),
                'right': 4,
                'left': 5
            }

            sprite_image = direction[self.direction]

        else:
            sprite_image = self.animation

        self.image = self.tileset.returnTile(sprite_image)
        self.rect = self.image.get_rect(topleft=self.pos)

        self.layer_name = "second"
        self.isit = "player"
