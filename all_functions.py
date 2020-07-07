import discord

def add_specified_to_inv(player_invs, ctx, item):
    person = str(ctx.author.id)
    person_inv = player_invs[person]
    person_inv.append(item)
    player_invs[person] = person_inv
    return "item added."

def read_inv(ctx, player_invs):
    person = str(ctx.author.id)
    if player_invs.get(person) != None:
        #await ctx.send("Looking through your inventory...")
        if len(player_invs[person]) != 0:
            return player_invs[person]
        else:
            return ["You have nothing atm."]
    else:
        return ["You do not have an inventory yet. Use 'new_inv' command to make one."]

def create_new_inventory(ctx, player_invs):
    person = str(ctx.author.id)
    if player_invs.get(person) == None: # if player does not have an inv
        player_invs.update({person:[]})
        return "New inventory initialised. \n You're all set."
    else:
        return "You already have an inventory. If you want to reset, use the reset command."

def ask_user_for_trade(player_invs, ctx, ongoing_trades, recipient, skin, trade_skin):
    person, recipient_name, recipient = str(ctx.author.id), str(recipient), str(recipient.id) # person is ALWAYS PERSON WHO STARTS TRADE
    trade = [person, recipient, skin, trade_skin] #always this TRADE STRUCTURE
    person_inv, recipient_inv = player_invs[person], player_invs[recipient]
    if skin in person_inv and trade_skin in recipient_inv and person!=recipient: #if they actually have skins, proceed
        ongoing_trades.append(trade)
        return "When " + recipient_name + " accepts the trade, the items will swap."
    else:
        return "That is an invalid trade."

def execute_trade(ctx, player_invs, ongoing_trades, starter, trade_skin, skin):
    person = str(ctx.author.id)
    starter = str(starter.id)
    person_inv = player_invs[person]
    starter_inv = player_invs[starter]
    # recipient/starter is actual person who STARTED trade
    trade = [starter, person, skin, trade_skin] # because people are swapped
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
