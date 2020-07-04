import discord

def add_specified_to_inv(player_invs, person, item):
    person_inv = player_invs[person]
    person_inv.append(item)
    player_invs[person] = person_inv
    return "item added."

def ask_user_for_trade(ongoing_trades, person, recipient_name, recipient, trade, person_inv, recipient_inv, skin, trade_skin):
    if skin in person_inv and trade_skin in recipient_inv and person!=recipient: #if they actually have skins, proceed
        ongoing_trades.append(trade)
        return "When " + recipient_name + " accepts the trade, the items will swap."
    else:
        return "That is an invalid trade."

def execute_trade(ongoing_trades, person, starter, person_inv, starter_inv, trade, player_invs, trade_skin, skin):
    if trade in ongoing_trades:
        skin_index = starter_inv.index(skin)
        trade_skin_index = person_inv.index(trade_skin)
        starter_inv[skin_index], person_inv[trade_skin_index] = person_inv[trade_skin_index], starter_inv[skin_index] # swap skins
        player_invs[starter], player_invs[person] = starter_inv, person_inv # update invs
        trade_index = ongoing_trades.index(trade)
        ongoing_trades.remove(trade)
        return "Trade complete."
    else:
        return "This trade hasn't been requested so you can't accept it? Lol. \n Request it if you want it."

def create_new_inventory(ctx, player_invs):
    person = str(ctx.author.id)
    if player_invs.get(person) == None: # if player does not have an inv
        player_invs.update({person:[]})
        return "New inventory initialised. \n You're all set."
    else:
        return "You already have an inventory. If you want to reset, use the reset command."
