import json
import gamestate

gs = json.load(open("./testdata/gamestate_full.json"))
print(gamestate.GameStateMessage(gs))

gs = json.load(open("./testdata/gamestate_diff.json"))
print(gamestate.GameStateMessage(gs))