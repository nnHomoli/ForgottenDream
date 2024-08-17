import pygame
import sys
from tilesetreader import tilesetRead


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, animation, direction, mapname, groups, cols, type):
        super().__init__(groups)
        self.tileset = tilesetRead('./mapdev/tileset/gameboy_rpg_v09.tsx')

        self.pos = pos
        if animation is None:
            directions = {
                'down': cols[0],
                'up': cols[1],
                'right': cols[2],
                'left': cols[3]
            }

            sprite_image = directions[direction]

        else:
            sprite_image = animation

        self.image = self.tileset.returnTile(sprite_image)
        self.rect = self.image.get_rect(topleft=pos)

        self.animation = animation
        self.direction = direction
        self.layer_name = 'second'
        self.isit = 'entity'
