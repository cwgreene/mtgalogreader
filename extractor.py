import mtgareader
import os
import json
import mtgagame

def setup_index():
    if not os.path.exists("cards.json"):
        raise Exception("Need to download cards.json from scryfall: https://scryfall.com/docs/api/bulk-data")
    with open("cards.json", encoding="utf8") as cards:
        cards = json.load(cards)

    mtga_index = {}
    for card in cards:
        if "arena_id" in card:
            mtga_index[card["arena_id"]] = card
    return mtga_index

index = setup_index()
mtga = mtgareader.parse_log()

game = mtga.games(index)[0]

i = 0
while game.next_state() is not None:
    print("\nState", i)
    game.show_state()
    i+=1