import os
import pygame
import pygame.gfxdraw
import pygame.mask
import numpy as np
from tile import Tile
from player import Player
from entity import Entity
from csvreader import Read_Map_CSV
from userDataManagment import ReadAndWrite

tile_size = 16


def on_screen(origin, sprite_position):
    display_size = pygame.display.get_surface().get_size()
    if ((0 <= sprite_position[0] - origin.pos[0] < display_size[0]) or (0 <= sprite_position[1] - origin.pos[1] < display_size[1]) or 
            (0 <= origin.pos[0] - sprite_position[0] < display_size[0]) and (0 <= origin.pos[1] - sprite_position[1] < display_size[1])):
        return True

    else:
        return False


class Level():
    def __init__(self, map):
        self.obstacle_sprites = pygame.sprite.Group()
        self.personal_sprites = []
        self.player = None
        self.mapname = map
        self.entity_graphics_outline_layers = {'events', 'third'}

        TILESIZE = tile_size

        self.fullmap = {}
        directory = os.listdir(f'./maps/{self.mapname}')

        for filename in directory:
            if filename.endswith('.csv'):
                layername = filename.replace(f'{self.mapname}_', '').replace('.csv', '')
                self.fullmap.update({layername: Read_Map_CSV(f'./maps/{self.mapname}/{filename}')})
            if filename == 'basemap.png':
                self.basemap = f'./maps/{self.mapname}/{filename}'

        self.visible_sprites = YSortCameraGroup(self.basemap)

        for layer_name, style in self.fullmap.items():
            for row_index, row in enumerate(style):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if layer_name == 'second':
                            Tile((x, y), "second", self.mapname, [self.visible_sprites], col)

                        if layer_name == 'events':
                            Tile((x, y), 'events', self.mapname, [self.visible_sprites], col, True)

                        if layer_name == 'third':
                            Tile((x, y), 'third', self.mapname, [self.visible_sprites], col)

                        if layer_name == 'invisible':
                            Tile((x, y), 'invisible', self.mapname, [self.obstacle_sprites], col, True)

        self.visible_sprites.update()

        print("--//MAPS: loaded - " + self.mapname)

    def render_player(self, udata):
        if self.personal_sprites is not None:
            self.visible_sprites.remove(
                [sprite for sprite in self.visible_sprites for personal in self.personal_sprites if sprite == personal])

        self.player = Player(udata, [self.visible_sprites, self.obstacle_sprites])

        self.render_personal_stuff(udata)
        self.entity_graphics_calculation(self.player)

        self.personal_sprites.append(self.player)
        self.visible_sprites.custom_draw(self.player)

    def render_personal_stuff(self, udata):
        user = ReadAndWrite(udata)

        personal = user.read('personal_sprites', self.player.slot)
        personal_ent = user.read('personal_entities', self.player.slot)
        party = user.read('party', self.player.slot)

        if personal is not None:
            for sprite in personal:
                if sprite[3] == self.mapname and on_screen(self.player, sprite[1]):
                    if isinstance(sprite[4], str):
                        if sprite[4] == "obstacle":
                            sprite[4] = [self.obstacle_sprites]

                        elif sprite[4] == "visible":
                            sprite[4] = [self.visible_sprites]

                    player_sprites = Tile(sprite[1], sprite[2], sprite[3], sprite[4], sprite[5])
                    self.personal_sprites.append(player_sprites)

        if personal_ent is not None:
            for entity_itself in personal_ent:
                if entity_itself[4] == self.mapname and on_screen(self.player, entity_itself[1]):
                    if isinstance(entity_itself[5], str):
                        if entity_itself[5] == "obstacle":
                            entity_itself[5] = [self.obstacle_sprites]

                        elif entity_itself[5] == "visible":
                            entity_itself[5] = [self.visible_sprites]

                    player_entity = Entity(entity_itself[1], entity_itself[2], entity_itself[3], entity_itself[4],
                                           entity_itself[5], entity_itself[6], entity_itself[7])

                    self.entity_graphics_calculation(player_entity)
                    self.personal_sprites.append(player_entity)

        if party is not None:
            for member in party:
                if on_screen(self.player, member[1]):
                    party_member = Entity(member[1], None, member[2], self.mapname, [self.visible_sprites], member[3],
                                          'party_character')

                    self.entity_graphics_calculation(party_member)
                    self.personal_sprites.append(party_member)

    def entity_graphics_calculation(self, whattype):
        for sprite in self.visible_sprites:
            if sprite.isit != whattype.isit and sprite.layer_name in self.entity_graphics_outline_layers and whattype.rect.colliderect(
                    sprite.rect):
                entity_mask = pygame.mask.from_surface(whattype.image)
                sprite_mask = pygame.mask.from_surface(sprite.image)
                entity_sprite = whattype.image.copy()
                rect = (sprite.rect.x - whattype.rect.x, sprite.rect.y - whattype.rect.y)

                overlap_mask = entity_mask.overlap_mask(sprite_mask, rect)
                overlap_surface = overlap_mask.to_surface(unsetcolor=(0, 0, 0, 0))

                outlined_points_entity = np.array(overlap_mask.outline(), dtype=np.int64)

                entity_sprite.blit(overlap_surface, rect, special_flags=pygame.BLEND_RGBA_SUB)

                outlined_entity_image = pygame.Surface(whattype.image.get_size(), pygame.SRCALPHA)
                pygame.gfxdraw.polygon(outlined_entity_image, outlined_points_entity, (255, 0, 255))
                outlined_entity_image.blit(entity_sprite, rect)

                whattype.image = outlined_entity_image


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, mapbase):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load(mapbase)
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        try:
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)
            pygame.display.update()

        except AttributeError as e:
            Warning(e)
            return
