import discord
def add_specified_to_inv(player_invs, person, item):
    person_inv = player_invs[person]
    person_inv.append(item)
    player_invs[person] = person_inv
    return "item added."
