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
    for card in cards:
        if "arena_id" not in card:
            continue
        if "card_faces" not in card:
            continue
        # HACK: Cant' seem to find any way to determine if the
        # card is double faced or not. Smitten Sword Master, for example
        # doesn't apply here, as it only has one side, and only one Arena Id.
        if card["arena_id"] + 1 not in mtga_index:
            mtga_index[card["arena_id"]+1] = card
    return mtga_index

index = setup_index()
mtga = mtgareader.parse_log()

game = mtga.games(index)[0]

i = 0
while game.next_state() is not None:
    print("\nState", i)
    game.show_state()
    i+=1