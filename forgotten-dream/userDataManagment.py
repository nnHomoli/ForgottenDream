import os
import random
import json
import threading
from queue import Queue
from pathlib import Path
from config import user_data, colliders_path

All_colliders = {}

if not os.path.exists(colliders_path):
    os.mkdir(colliders_path)

if not os.path.exists(user_data):
    os.mkdir(user_data)

for collision in os.listdir(colliders_path):
    if collision.endswith('.json'):
        with open(colliders_path + "/" + collision, 'r') as colliders_read:
            collide_data = colliders_read.read()
            colliders_parsed = json.loads(collide_data)
            collider_name = collision.replace('.json', '')
            All_colliders.update({collider_name: colliders_parsed})


class ReadAndWrite:
    def __init__(self, uuid):
        self.uid = uuid
        self.CollisionQueue = Queue()
        self.AngelQueue1 = Queue()
        self.AngelQueue2 = Queue()

    def register(self, user_preferred):

        file_path = Path(f'{user_data}/[{self.uid}].txt')
        if file_path.exists():
            return 'your data already exist'

        data = {}
        data['language'] = user_preferred
        data['menu'] = 'menu_start_on'
        data['last_menu'] = None
        data['current_slot'] = None
        data['debug'] = 'False'
        data['x2_mode'] = 'False'

        with open(f'{user_data}/[{self.uid}].json', 'w') as user:
            json.dump(data, user, indent=4)

        return "You've been successfully registered"

    def register_slot(self, slot_number, name):
        profile_check = Path(f"{user_data}/[{self.uid}].json")
        if not profile_check.exists():
            return "player has no profile"

        check_slot = Path(f"{user_data}/[{self.uid}_{slot_number}].json")
        if check_slot.exists():
            return "slot is unavailable"

        slot_data = {}
        slot_data['name'] = name
        slot_data['???_value'] = random.randint(1, 20)
        slot_data['pos'] = (352, 352)
        slot_data['animation'] = None
        slot_data['direction'] = 'down'
        slot_data['inventory'] = None
        slot_data['map'] = 'screenburninExtended'
        slot_data['personal_sprites'] = None
        slot_data['personal_entities'] = None
        slot_data['party'] = None

        with open(f'{user_data}/[{self.uid}_{slot_number}].json', 'w') as user:
            json.dump(slot_data, user, indent=4)

    def ChangeValue(self, target_content, changes, slot='none'):
        if slot == 'none':
            pathToData = f'{user_data}/[{self.uid}].json'
        else:
            pathToData = f'{user_data}/[{self.uid}_{slot}].json'
        with open(pathToData, 'r') as file:
            data = json.load(file)

        data[target_content] = changes

        with open(pathToData, 'w') as file:
            json.dump(data, file, indent=4)

    def delete_sprite(self, personal_type, sprite_call, slot):
        path = f'{user_data}/[{self.uid}_{slot}].json'
        if not Path(path).exists():
            return

        with open(path, 'r') as readfile:
            json_itself = json.load(readfile)

        if personal_type == 'sprite':
            for sprite in json_itself['personal_sprites']:
                if sprite[0] == sprite_call:
                    json_itself['personal_sprites'].remove(sprite)

        elif personal_type == 'entity':
            for entity in json_itself['personal_entities']:
                if entity[0] == sprite_call:
                    json_itself['personal_entities'].remove(entity)

        elif personal_type == 'party':
            for entity in json_itself['party']:
                if entity[0] == sprite_call:
                    json_itself['party'].remove(entity)

        with open(path, 'w') as file:
            json.dump(json_itself, file, indent=4)

    def get_sprite_properties(self, persona_type, call, properties, slot):
        path = f'{user_data}/[{self.uid}_{slot}].json'
        if not Path(path).exists():
            return

        with open(path, 'r') as readfile:
            json_itself = json.load(readfile)

        if persona_type == 'sprite':

            properties_data = {
                'call': 0,
                'pos': 1,
                'layer': 2,
                'map': 3,
                'groups': 4,
                'col': 5,
                'collidable': 6
            }

            for sprite in json_itself['personal_sprites']:
                if sprite[0] == call:
                    return sprite[properties_data[properties]]
            return None

        elif persona_type == 'entity':

            properties_data = {
                'call': 0,
                'pos': 1,
                "animation": 2,
                'direction': 3,
                'map': 4,
                'groups': 5,
                'cols': 6,
                'type': 7
            }

            for entity in json_itself['personal_entities']:
                if entity[0] == call:
                    return entity[properties_data[properties]]
            return None

    def change_sprite_properties(self, personal_type, sprite_call, properties, changes, slot):
        path = f'{user_data}/[{self.uid}_{slot}].json'
        if not Path(path).exists():
            return

        with open(path, 'r') as readfile:
            json_itself = json.load(readfile)

        if personal_type == 'sprite':
            properties_data = {
                'call': 0,
                'pos': 1,
                'layer': 2,
                'map': 3,
                'groups': 4,
                'col': 5,
                'collidable': 6
            }

            for sprite in json_itself['personal_sprites']:
                if sprite[0] == sprite_call:
                    sprite[properties_data[properties]] = changes

        elif personal_type == 'entity':
            properties_data = {
                'call': 0,
                'pos': 1,
                'animation': 2,
                'direction': 3,
                'map': 4,
                'groups': 5,
                'cols': 6,
                'type': 7
            }

            for sprite in json_itself['personal_entities']:
                if sprite[0] == sprite_call:
                    sprite[properties_data[properties]] = changes

        elif personal_type == 'party':
            properties_data = {
                'call': 0,
                'pos': 1,
                'direction': 2,
                'cols': 3
            }

            for sprite in json_itself['party']:
                if sprite[0] == sprite_call:
                    sprite[properties_data[properties]] = changes

        with open(path, 'w') as file:
            json.dump(json_itself, file, indent=4)

    def delete_from_inventory(self, item_name, slot):
        path = f'{user_data}/[{self.uid}_{slot}].json'
        if not Path(path).exists():
            return

        with open(path, 'r') as readfile:
            json_itself = json.load(readfile)

        for item in json_itself['inventory']:
            if item[0] == item_name:
                json_itself['inventory'].remove(item)

        with open(path, 'w') as file:
            json.dump(json_itself, file, indent=4)

    def AppendValue(self, collumn, custom_value, slot='none'):
        if slot != 'none':
            with open(f'{user_data}/[{self.uid}_{slot}].json', 'r') as file:
                data = json.load(file)

        else:
            with open(f'{user_data}/[{self.uid}].json', 'r') as file:
                data = json.load(file)

        values = data.get(collumn)
        if values is not None:
            values.append(custom_value)
        else:
            data[collumn] = [custom_value]

        if slot != 'none':
            with open(f'{user_data}/[{self.uid}_{slot}].json', 'w') as file:
                json.dump(data, file, indent=4)

        else:
            with open(f'{user_data}/[{self.uid}].json', 'w') as file:
                json.dump(data, file, indent=4)

    def GetValues(self, collumn, slot='none'):
        if slot != 'none':
            with open(f'{user_data}/[{self.uid}_{slot}].json', 'r') as file:
                data = json.load(file)

        else:
            with open(f'{user_data}/[{self.uid}].json', 'r') as file:
                data = json.load(file)
        return data[collumn]

    def MovePlayerPosBy(self, pos):
        if pos == (0, 0):
            return

        AngelChecks = False
        Angelpass = False
        Angel1NO = False
        Angel2NO = False

        while not self.CollisionQueue.empty():
            last, call = self.CollisionQueue.get()
            del last, call

        gameSlot = self.read('current_slot')
        mapname = self.read('map', gameSlot)
        party = self.read('party', gameSlot)
        initial_pos = self.read("pos", gameSlot)
        initial_direction = self.read("direction", gameSlot)
        final_pos = (initial_pos[0] + pos[0], initial_pos[1] + pos[1])
        pos_check = str(final_pos)

        final_pos_latest = final_pos

        check = threading.Thread(target=self.check_colliders, args=(pos_check, self.CollisionQueue, mapname, gameSlot,))
        check.start()

        if pos[0] != 0 and pos[1] != 0:
            pos_check1 = (final_pos[0], initial_pos[1])
            pos_check2 = (initial_pos[0], final_pos[1])

            check1 = threading.Thread(target=self.check_colliders,
                                      args=(str(pos_check1), self.AngelQueue1, mapname, gameSlot,))
            check2 = threading.Thread(target=self.check_colliders,
                                      args=(str(pos_check2), self.AngelQueue2, mapname, gameSlot,))
            check1.start()
            check2.start()

            AngelChecks = True

        direction = {
            pos[0] < 0: 'left',
            pos[0] > 0: 'right',
            pos[1] > 0: 'down',
            pos[1] < 0: 'up'
        }

        with open(f'{user_data}/[{self.uid}_{gameSlot}].json', 'r') as data:
            data = json.load(data)

            check.join()

            if AngelChecks:
                check1.join()
                check2.join()
                final_pos_latest = list(final_pos_latest)
                if not self.AngelQueue1.empty():
                    self.AngelQueue1.get()
                    final_pos_latest[0] = initial_pos[0]
                    Angel1NO = True
                if not self.AngelQueue2.empty():
                    self.AngelQueue2.get()
                    final_pos_latest[1] = initial_pos[1]
                    Angel2NO = True

                if final_pos_latest == initial_pos:
                    return
                if not self.CollisionQueue.empty() and not Angel1NO and not Angel2NO:
                    final_pos_latest[0] = initial_pos[0]

                tuple(final_pos_latest)

                if self.CollisionQueue.empty() and Angel1NO and not Angel2NO or self.CollisionQueue.empty() and not Angel1NO and Angel2NO:
                    final_pos_latest = final_pos

                Angelpass = True

            if self.CollisionQueue.empty() or Angelpass:
                data['pos'] = final_pos_latest

                member_properties = None
                if data['party'] is not None:
                    for member in data['party']:
                        saved_member_properties = member[1], member[2]

                        member[1] = initial_pos if member_properties is None else member_properties[0]
                        member[2] = initial_direction if member_properties is None else member_properties[1]

                        member_properties = saved_member_properties

            else:
                if AngelChecks:
                    pass

                else:
                    last, callback = self.CollisionQueue.get()
                    del last

                    return callback

            data['direction'] = direction.get(True)
        with open(f'{user_data}/[{self.uid}_{gameSlot}].json', 'w') as data_final:
            json.dump(data, data_final, indent=4)
        return None

    def read(self, variable, slot='none'):
        if slot == 'none':
            userDataPath = f'{user_data}/[{self.uid}].json'
        else:
            userDataPath = f'{user_data}/[{self.uid}_{slot}].json'
        try:
            with open(userDataPath, 'r') as data:
                data = json.load(data)
                return data[variable]

        except FileNotFoundError as e:
            raise Warning(e)

    def check_personal_colliders(self, Que, pos, slot):
        sprites = self.read('personal_sprites', slot)
        if not sprites:
            return

        current_map = self.read('map', slot)

        for sprite in sprites:
            if sprite[3] == current_map and str((sprite[1][0], sprite[1][1])) == pos and sprite[6] == 'True':
                Que.put((True, sprite[0]))

                break

    def check_entity_colliders(self, Que, pos, slot):
        entities = self.read('personal_entities', slot)
        if not entities:
            return

        current_map = self.read('map', slot)

        for entity in entities:
            if entity[4] == current_map and str((entity[1][0], entity[1][1])) == pos and entity[7] == 'standby':
                Que.put((True, entity[0]))

                break

    def check_colliders(self, pos, que, mapname, slot):
        personal_check = threading.Thread(target=self.check_personal_colliders, args=(que, pos, slot,))
        entity_check = threading.Thread(target=self.check_entity_colliders, args=(que, pos, slot,))

        personal_check.start()
        entity_check.start()

        collidermap = All_colliders.get(mapname)
        for row in collidermap.values():
            if any(pos in value for value in row):
                que.put((True, row[0]))
                break

        personal_check.join()
        entity_check.join()
