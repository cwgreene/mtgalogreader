# Game State Strucutre
# {
#    "type"
# }

def opt(json, key, func, default=None):
    if key in json:
        return func(key)
    return default

class JsonSpec(object):
    def parse(self, json):
        for attr in self.__dict__:
            attr_value = getattr(self, attr)
            if type(attr_value) == type(int):
                setattr(self, attr, attr_value(json[attr]))

class DeckConstraintInfo(JsonSpec):
    def __init__(self, json):
        self.minDeckSize = int
        self.maxDeckSize = int
        self.maxSideboardSize = int
        self.parse(json)

class Team(object):
    def __init__(self, json):
        self.id = int(json["id"])
        self.playerIds = [int(id) for id in json["playerIds"]]

class GameInfo(object):
    def __init__(self, json):
        self.matchID = str(json["matchID"])
        self.gameNumber = int(json["gameNumber"])
        self.stage = str(json["stage"])
        self.type = str(json["type"])
        self.variant = str(json["variant"])
        self.matchState = str(json["matchState"])
        self.matchWinCondition = str(json["matchWinCondition"])
        self.maxTimeoutCount = int(json["maxTimeoutCount"])
        self.maxPipCount = int(json["maxPipCount"])
        self.timeoutDurationSec = int(json["timeoutDurationSec"])
        self.superFormat = str(json["superFormat"])
        self.mulliganType =  str(json["mulliganType"])
        self.deckConstraintInfo = DeckConstraintInfo(json["deckConstraintInfo"])

class GameObject(object):
    def __init__(self, json):
        self.instanceId = int(json["instanceId"])
        self.grpId = int(json["grpId"])
        self.type = str(json["type"])
        self.zoneId = int(json["zoneId"])
        self.visibility = str(json["visibility"])
        self.ownerSeatId = str(json["ownerSeatId"])
        self.controllerSeatId = str(json["controllerSeatId"])
        self.cardTypes = [str(type) for type in json.get("cardTypes", [])]
        self.subtypes = [str(type) for type in json.get("subtypes", [])]
        self.color = [str(type) for type in json.get("color", [])]
        self.power = json.get("power", None)
        self.toughness = json.get("toughness", None)
        self.viewers = [int(viewer) for viewer in json.get("viewers", [])]
        self.name = int(json["name"]) if "name" in json else None
        self.ability = [int(ability) for ability in json.get("abilities", [])]
        self.overlayGrpId = opt(json, 'overlayGrpId', lambda k: json[k])

class Zone(object):
    def __init__(self, json):
        self.zoneId = int(json["zoneId"])
        self.type = str(json["type"])
        self.visibility = str(json["visibility"])
        self.ownerSeatId = int(json["ownerSeatId"]) if "ownerSeatId" in json else 0
        self.objectInstanceIds = [json.get(id) for id in json.get("objectInstanceIds", [])]
        self.viewers = [int(id) for id in json.get("viewers", [])]

class Player(object):
    def __init__(self, json):
        self.lifeTotal = int(json["lifeTotal"])
        self.systemSeatNumber = int(json["systemSeatNumber"])
        self.maxHandSize = int(json["maxHandSize"])
        self.teamId = int(json["teamId"])
        self.timerIds = [int(timerId) for timerId in json.get("timerIds", [])]
        self.controllerSeatId = int(json["controllerSeatId"])
        self.controllerType = str(json["controllerType"])
        self.pendingMessageType = str(json["pendingMessageType"]) if "pendingMessageType" in json else None
        self.startingLifeTotal = int(json["startingLifeTotal"])

class TurnInfo(object):
    def __init__(self, json):
        self.decisionPlayer = opt(json, "decisionPlayer", lambda k: int(json[k]))
        self.phase = opt(json, "phase", lambda k: str(json[k]))
        self.step = opt(json, "step", lambda k: str(json[k]))
        self.turnNumber = opt(json, "turnNumber", lambda k: int(json[k]))
        self.activePlayer = opt(json, "activePlayer", lambda k: int(json[k]))
        self.priorityPlayer = opt(json, "priorityPlayer", lambda k: int(json[k]))
        self.nextPhase = opt(json, "nextPhase", lambda k: str(json[k]))
        self.nextStep = opt(json, "nextStep", lambda k: str(json[k]))

class Annotation(object):
    def __init__(self, json):
        self.id = int(json["id"])
        self.affectorId = int(json["affectorId"]) if "affectorId" in json else None
        self.affectedIds = [int(id) for id in json.get("affectedIds", [])]
        self.type = [str(type) for type in json["type"]]

class Timer(object):
    def __init__(self, json):
        self.timerId = int(json["timerId"])
        self.type = str(json["type"])
        self.durationSec = int(json["durationSec"])
        self.behavior = str(json["behavior"])
        self.warningThresholdSec = str(json["warningThresholdSec"]) if "warningThresholdSec" in json else None

class GameStateMessage(object):
    def __init__(self, json):
        self.type = str(json["type"])
        self.gamesStateId = int(json["gameStateId"])
        self.gameInfo = GameInfo(json["gameInfo"]) if "gameInfo" in json else None
        self.teams = [Team(team) for team in json.get("teams", [])]
        self.players = [Player(player) for player in json.get("players", [])]
        self.turnInfo = TurnInfo(json["turnInfo"]) if "turnInfo" in json else None
        self.zones = [Zone(zone) for zone in json.get("zones", [])]
        self.gameObjects = [GameObject(gameObject) for gameObject in json.get("gameObjects", [])]
        self.annotations = [Annotation(annotation) for annotation in json.get("annotations", [])]
        self.diffDeletedInstanceIds = [diff for diff in json.get("diffDeletedInstanceIds", [])]
        self.pendingMessageCount = int(json.get("pendingMessageCount",0))
        self.prevGameStateId = int(json["prevGameStateId"]) if "prevGameStateId" in json else None
        self.timers = [Timer(timer) for timer in json.get("timers", [])]
        self.update = str(json["update"])
        self.actions = [action for action in json.get("actions", [])]


class GameState(object):
    def __init__(self, json):
        self.json = json.copy()
    
    def update(self, diffjson):
        # validate this is update diff
        pass