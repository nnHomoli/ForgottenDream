import pygame
import json
from pathlib import Path
from config import colliders_path
from tilesetreader import tilesetRead


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, layer_name, mapname, groups, col, collidable=False):
        super().__init__(groups)
        self.tileMap = tilesetRead('./mapdev/tileset/gameboy_rpg_v09.tsx')

        self.col = int(col)

        self.image = self.tileMap.returnTile(self.col)
        self.rect = self.image.get_rect(topleft=pos)
        self.mapname = mapname
        self.layer_name = layer_name
        self.pos = pos
        self.isit = "tile"

        if collidable:
            append_collider(col, pos, self.mapname)


def append_collider(col, pos, mapname):
    check_file = Path(f'{colliders_path}/{mapname}.json')
    outputFile = f'{colliders_path}/{mapname}.json'
    pos = str(pos)

    if check_file.exists():
        with open(outputFile, 'r') as colliders_read:
            collide_data = json.load(colliders_read)
            values = collide_data.get(col)

        if col in collide_data and col not in values:
            if pos not in values:
                values.append(pos)

        if col not in collide_data:
            collide_data[col] = [f"{col}_generalcallback", pos]

    else:
        collide_data = {
            col: [f"{col}_generalcallback", pos],
        }

    with open(outputFile, 'w') as colliders:
        json.dump(collide_data, colliders, indent=4)
