import gamestate

import typing
from typing import _GenericAlias, List

class MTGAGame(object):
    def __init__(self, gamestates : List[gamestate.GameStateMessage], cards):
        initial = gamestates[0]
        self.game_states = gamestates
        self.cards = cards
        self.zone_map = { zone.zoneId : zone for zone in initial.zones}
        self.game_objects = { game_object.instanceId : game_object for game_object in initial.gameObjects }
        self.state_index = 0
        self.annotations = initial.annotations
        self.turn_info = initial.turnInfo
    
    def show_state(self):
        print(self.turn_info)
        for zoneId in self.zone_map:
            zone = self.zone_map[zoneId]
            if [objId for objId in zone.objectInstanceIds if objId in self.game_objects]:
                print(zone.type, "({})".format(zone.ownerSeatId))
            for objKey in zone.objectInstanceIds:
                if objKey in self.game_objects:
                    obj = self.game_objects[objKey]
                    if obj.grpId in self.cards:
                        objectText = self.cards[obj.grpId]["name"]
                    else:
                        sourceId = obj.objectSourceGrpId
                        if sourceId in self.cards:
                            source = self.cards[sourceId]["name"]
                        else:
                            source = sourceId
                        objectText = "[{} {} from {}]".format(obj.grpId, obj.type, source)
                    owner = obj.controllerSeatId
                    print(" -", "{} ({}) [{}]".format(objectText, owner, obj.instanceId))
        for annotation in self.annotations:
            print(annotation)
    
    def next_state(self):
        if self.state_index + 1 >= len(self.game_states):
            return None
        self.state_index += 1
        state = self.game_states[self.state_index]
        
        zone_map = { zone.zoneId : zone for zone in state.zones}
        game_objects = { game_object.instanceId : game_object for game_object in state.gameObjects }
        self.game_objects.update(game_objects)
        self.turn_info = state.turnInfo

        self.zone_map.update(zone_map)
        self.annotations = state.annotations
                
        for deleted_id in state.diffDeletedInstanceIds:
            if deleted_id not in self.game_objects:
                continue
            self.game_objects.pop(deleted_id)

        return self.state_index