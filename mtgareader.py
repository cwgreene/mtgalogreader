import os
import json
import re

MTGA_PATH = os.path.join(os.path.expanduser("~"),"AppData","LocalLow","Wizards of the Coast","MTGA")

# REGEXS
## [UnityCrossThreadLogger]11/7/2020 4:20:18 PM: LNUXWA65ZVFBPBW4JRSB5C54ZI to Match: ClientToMatchServiceMessageType_ClientToGREUIMessage
GAME_MESSAGE = r"\[UnityCrossThreadLogger\][^ ]* [^ ]* [AP]M: ([^ ]* to Match|Match to [^ ]*): (?P<message_type>.*$)"
LOG_HEADER = r"^\[(?P<log_type>[^\[]*)\].*"

LOG_TYPES=[GAME_MESSAGE]

def trans_parse(state, line, log_type):
    # add copy of header, log_type, body to accumulator
    state["acc"].append(state["state"].copy())

    # reset state
    state["state"]["log_type"] = log_type
    state["state"]["body"] = ""
    state["state"]["header"] = line

def check_new_log_type(state, line):
    match = re.match(LOG_HEADER, line)
    if match:
        log_type = match.groupdict()["log_type"]
        trans_parse(state, line, log_type)
        return state
    else:
        state["state"]["body"] += line
        return state

def parse_log_line(state, line):
    state = check_new_log_type(state, line)
    return state

def read_player_log():
    state = {"state": {"header": None, "log_type": None, "body":""}, "acc":[]}
    state_sets = set()
    with open(os.path.join(MTGA_PATH,"Player.log"), encoding="utf8") as playerlog:
        for line in playerlog.readlines():
            state = parse_log_line(state, line)
    for log in state["acc"][1:]:
        match = re.match(GAME_MESSAGE, log["header"])
        if match:
            message_type = match.groupdict()["message_type"]
            if message_type == "GreToClientEvent":
                try:
                    json.loads(log["body"].split("\n")[0])
                except:
                    print("failure")
                    print(log["body"])
            state_sets.add(message_type)
    print(state_sets)
read_player_log()