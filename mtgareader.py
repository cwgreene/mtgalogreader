import os
import json
import re

MTGA_PATH = os.path.join(os.path.expanduser("~"),"AppData","LocalLow","Wizards of the Coast","MTGA")

# REGEXS
## [UnityCrossThreadLogger]11/7/2020 4:20:18 PM: LNUXWA65ZVFBPBW4JRSB5C54ZI to Match: ClientToMatchServiceMessageType_ClientToGREUIMessage

LOG_HEADER = r"^\[(?P<log_type>[^\[]*)\].*"

# Game messages formats
GAME_MESSAGE = r"\[UnityCrossThreadLogger\][^ ]* [^ ]* [AP]M: ([^ ]* to Match|Match to [^ ]*): (?P<message_type>.*$)"
MULTI_LINE_JSON = set(["ClientToMatchServiceMessageType_ClientToGREMessage", "ClientToMatchServiceMessageType_ClientToGREUIMessage"])
SINGLE_LINE_JSON = set(["GreToClientEvent", "AuthenticateResponse", "MatchGameRoomStateChangedEvent", "Error"])

# IncomingMessage formats
INCOMING_API_MESSAGE = r"\[UnityCrossThreadLogger\]<== (?P<api_name>[^ ]*) (?P<json_payload>.*)$"

LOG_PARSERS={
    "GAME_MESSAGE": {
        "matcher": GAME_MESSAGE,
        "handler": lambda match, log: parse_game_message(match.groupdict()["message_type"], log["header"], log["body"])
    },
    "INCOMING_API_MESSAGE": {
        "matcher": INCOMING_API_MESSAGE,
        "handler": lambda match, log: {
                "type": "api_message_response", 
                "subtype": match.groupdict()["api_name"],
                "json": json.loads(match.groupdict()["json_payload"])["payload"]
            }
    }
}

class MTGALog(object):
    def __init__(self, logs):
        self.logs = logs

    def filter(self, **kwargs):
        new_logs = []
        for log in self.logs:
            match = True
            for kwarg in kwargs:
                if kwarg not in log:
                    raise Exception("{} not a valid filter", kwarg)
                if log[kwarg] != kwargs[kwarg]:
                    match = False
                    break
            if match:
                new_logs.append(log)
        return MTGALog(new_logs)

    def __repr__(self):
        return repr(self.logs)
    
    def __str__(self):
        return str(self.logs)

    def __getitem__(self, key):
        return self.logs[key]

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

def parse_initial_json(data):
    # it's '+ 2' because \n is +1 past the index, and \n} is +2
    end_json = data.find("\n}\n") + 2
    return json.loads(data[:end_json]), end_json

def parse_game_message(message_type, header, body):
    if message_type in MULTI_LINE_JSON:
        try:
            js, end_json = parse_initial_json(body)
            rest = body[end_json]
        except:
            print(body)
            raise('Failure')
    elif message_type in SINGLE_LINE_JSON:
        lines = body.split("\n")
        js = lines[0]
        rest = "\n".join(lines[1:])
    else:
        print(body)
        raise(Exception("Can't handle message type {} [{}]: {}".format(message_type, header, body)))
    return {
        "type": "game_message",
        "subtype": message_type,
        "json":js,
        "rest":rest
    }

def parse_log():
    state = {"state": {"header": None, "log_type": None, "body":""}, "acc":[]}
    state_sets = set()
    with open(os.path.join(MTGA_PATH,"Player.log"), encoding="utf8") as playerlog:
        for line in playerlog.readlines():
            state = parse_log_line(state, line)
    parsed_logs = []
    for log in state["acc"][1:]:
        for log_parser in LOG_PARSERS:
            match = re.match(LOG_PARSERS[log_parser]["matcher"], log["header"])
            if match:
                parsed_logs.append(LOG_PARSERS[log_parser]["handler"](match, log))
    return MTGALog(parsed_logs)
