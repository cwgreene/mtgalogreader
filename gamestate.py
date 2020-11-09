# Game State Strucutre
# {
#    "type"
# }
import typing
from typing import _GenericAlias, List

def opt(json, key, func, default=None):
    if key in json:
        return func(key)
    return default


class Optional(object):
    def __init__(self, t, default=None):
        self.type = t
        self.default = default

class JsonSpec(object):
    def parse(self, json):
        for attr in self.__dict__:
            try:
                attr_value = getattr(self, attr)
                # we should probably be recursive here; but oh well. No Optional(Optional)
                if type(attr_value) == Optional:
                    if attr not in json:
                        setattr(self, attr, attr_value.default)
                        continue
                    attr_value = attr_value.type
                    #print(attr_value, json)
                
                # Optional falls through here. json[attr] should exist now.
                if type(attr_value) == type:
                    setattr(self, attr, attr_value(json[attr]))
                elif type(attr_value) == _GenericAlias: # assume it's a list for now
                    element_constructor = typing.get_args(attr_value)[0]
                    array = [element_constructor(e) for e in json.get(attr, [])]
                    setattr(self, attr, array)
            except Exception as e:
                raise Exception("Error parsing {}".format(attr)) from e
                
    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

class DeckConstraintInfo(JsonSpec):
    def __init__(self, json):
        self.minDeckSize = int
        self.maxDeckSize = int
        self.maxSideboardSize = int

        self.parse(json)

class Team(JsonSpec):
    def __init__(self, json):
        self.id = int
        self.playerIds = List[int]

        self.parse(json)

class GameInfo(JsonSpec):
    def __init__(self, json):
        self.matchID = str
        self.gameNumber = int
        self.stage = str
        self.type = str
        self.variant = str
        self.matchState = str
        self.matchWinCondition = str
        self.maxTimeoutCount = int
        self.maxPipCount = int
        self.timeoutDurationSec = int
        self.superFormat = str
        self.mulliganType =  str
        self.deckConstraintInfo = DeckConstraintInfo

        self.parse(json)

class GameObject(JsonSpec):
    def __init__(self, json):
        self.instanceId = int
        self.grpId = int
        self.type = str
        self.zoneId = int
        self.visibility = str
        self.ownerSeatId = str
        self.controllerSeatId = str
        self.cardTypes = List[str]
        self.subtypes = List[str]
        self.color = List[str]
        self.power = Optional(dict)
        self.toughness = Optional(dict)
        self.viewers = List[int]
        self.name = Optional(int)
        self.ability = List[int]
        self.overlayGrpId = Optional(int)

        self.parse(json)

class Zone(JsonSpec):
    def __init__(self, json):
        self.zoneId = int
        self.type = str
        self.visibility = str
        self.ownerSeatId = Optional(int)
        self.objectInstanceIds = List[int]
        self.viewers = List[int]

        self.parse(json)
    
class Player(JsonSpec):
    def __init__(self, json):
        self.lifeTotal = int
        self.systemSeatNumber = int
        self.maxHandSize = int
        self.teamId = int
        self.timerIds = List[int]
        self.controllerSeatId = int
        self.controllerType = str
        self.pendingMessageType = Optional(str)
        self.startingLifeTotal = int

        self.parse(json)

class TurnInfo(JsonSpec):
    def __init__(self, json):
        self.decisionPlayer = Optional(int)
        self.phase = Optional(str)
        self.step = Optional(str)
        self.turnNumber = Optional(int)
        self.activePlayer = Optional(int)
        self.priorityPlayer = Optional(int)
        self.nextPhase = Optional(str)
        self.nextStep = Optional(str)

        self.parse(json)

class Annotation(JsonSpec):
    def __init__(self, json):
        self.id = int
        self.affectorId = Optional(int)
        self.affectedIds = List[int]
        self.type = List[str]

        self.parse(json)

class Timer(JsonSpec):
    def __init__(self, json):
        self.timerId = int
        self.type = str
        self.durationSec = int
        self.behavior = str
        self.warningThresholdSec = Optional(str)

        self.parse(json)

class MonoManaCost(JsonSpec):
    def __init__(self, json):
        self.color = List[str]
        self.count = int

        self.parse(json)

class Action(JsonSpec):
    def __init__(self, json):
        self.actionType = str
        self.instanceId = Optional(int)
        self.manaCost = List[MonoManaCost]

        self.parse(json)

class ActionSeat(JsonSpec):
    def __init__(self, json):
        self.seatId = int
        self.action = Action
        
        self.parse(json)

class GameStateMessage(JsonSpec):
    def __init__(self, json):
        self.type = str
        self.gameStateId = int
        self.gameInfo = Optional(GameInfo)
        self.teams = List[Team]
        self.players = List[Player]
        self.turnInfo = Optional(TurnInfo)
        self.zones = List[Zone]
        self.gameObjects = List[GameObject]
        self.annotations = List[Annotation]
        self.diffDeletedInstanceIds = List[int]
        self.pendingMessageCount = Optional(int, 0)
        self.prevGameStateId = Optional(int)
        self.timers = List[Timer]
        self.update = str
        self.actions = List[ActionSeat]

        self.parse(json)

class GameState(object):
    def __init__(self, json):
        self.json = json.copy()
    
    def update(self, diffjson):
        # validate this is update diff
        pass