import mtgareader
import os
import json

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
for log in mtga.logs:
    print(log["subtype"])
print(mtga.games())
cards_db = mtga.filter(subtype="PlayerInventory.GetPlayerCardsV3")[-1]["json"]
"""
for card_id in cards_db:
    if int(card_id) in index:
        card = index[int(card_id)]
        print(card["name"], cards_db[card_id])
    else:
        raise(Exception("Could not find {}".format(card_id)))"""