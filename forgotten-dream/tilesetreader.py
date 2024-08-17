import os
import pygame
from bs4 import BeautifulSoup


class tilesetRead:
    def __init__(self, tsxlocation):
        self.tsxlocation = tsxlocation
        self.samedir = os.path.dirname(tsxlocation)

        self.TileImage = self.returnProperties('image', 'source')
        self.ImageDIR = os.path.join(self.samedir, self.TileImage)

    def returnProperties(self, properties, attribute_properties):
        with open(self.tsxlocation, 'r') as tsxRaw:
            tsxfile = tsxRaw.read()

        soup = BeautifulSoup(tsxfile, 'xml')
        var = soup.find(properties)

        if var is not None:
            val = var.get(attribute_properties)
            return val

        return None

    def returnTile(self, tileUID):
        Tilewidth = int(self.returnProperties('tileset', 'tilewidth'))
        ImageWidth = int(self.returnProperties('image', 'width'))
        ImageHeight = int(self.returnProperties('image', 'height'))
        tileset_image = pygame.image.load(self.ImageDIR)

        tiles = {}

        TILE_SIZE = Tilewidth

        for y in range(tileset_image.get_height() // TILE_SIZE):
            for x in range(tileset_image.get_width() // TILE_SIZE):
                tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                tile_image = pygame.Surface(tile_rect.size, pygame.SRCALPHA)
                tile_image.blit(tileset_image, (0, 0), tile_rect)
                tile_id = y * (tileset_image.get_width() // TILE_SIZE) + x
                tiles[tile_id] = tile_image

        return tiles.get(tileUID)
