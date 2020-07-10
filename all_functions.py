import discord
import random

def add_specified_to_inv(player_invs, ctx, item):
    person = str(ctx.author.id)
    person_inv = player_invs[person]
    person_inv.append(item)
    player_invs[person] = person_inv
    return "item added."

def read_inv(ctx, player_invs, person):
    if person != None:
        person = str(person.id)
        print("The person var = ", person)
    else:
        person = str(ctx.author.id)
        print("person is author")
    print("a", person)
    if player_invs.get(person) != None:
        #await ctx.send("Looking through your inventory...")
        if len(player_invs[person]) != 0:
            return ', '.join(player_invs[person])
        else:
            return "Nothing in there atm."
    else:
        return "No inventory yet. Use 'new_inv' command to make one."

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

def get_item(list_name):
    item = list_name[random.randint(0, len(list_name)-1)] #-1 because indexing starts with 0
    return item

def spin_roulette(ctx, player_invs):
    randnum = random.randint(0, 100)
    if randnum > 60:
        uncommon_list = ["aqua", "bark auto", "blushed mma", "carbon mmr", "commo", "digital auto", "dropper"]
        #item = "uncommon"
        item = get_item(uncommon_list)
        gif = 'uncommon.gif'
        statement = "You got " + item #make it display different gifs
    elif 30 < randnum <= 60:
        rare_list = ["artic auto", "auto machinist", "autumn auto", "bloodripper", "flecken auto", "hazard auto", "jade", "kodac auto"]
        #item = "rare"
        item = get_item(rare_list)
        gif = 'rare.gif'
        statement = "You got " + item
    elif 15 < randnum <= 30:
        epic_list = ["black ice", "barbed auto", "blaze auto", "m14 chartreuse", "mma cygento", "mma octo"]
        #item = "epic"
        item = get_item(epic_list)
        gif = 'epic.gif'
        statement = "You span " + item
    elif 7 < randnum <= 15:
        legendary_list = ["magnis", "shot element", "acid breath", "101 skullbreaker", "haste", "lava bolt"]
        #item = "legendary"
        item = get_item(legendary_list)
        gif = 'legendary.gif'
        statement = "Legendary " + item + "!"
    elif 3 < randnum <= 7:
        relic_list = ["mma plasma", "neuromance", "awp pacemaker", "awp stream", "neon reaver", "razor"]
        #item = "relic"
        item = get_item(relic_list)
        gif = 'relic.gif'
        statement = "Nice, you got relic - " + item
    elif 1 < randnum <= 3:
        contraband_list = ["raynb0w", "1ad-da0", "xon-vox", "exos", "futuristic", "izula", "hackusate", "pellucid"]
        #item = "contraband"
        item = get_item(contraband_list)
        gif = 'contraband.gif'
        statement = "You got " + item
    else:
        unobtainable_list = ["disintegrator", "anti-matter", "wutdatime_exclusive"]
        #item = "unobtainable"
        item = get_item(unobtainable_list)
        gif = 'unobtainable.gif'
        statement = "Wow. Unobtainable - " + item
    add_specified_to_inv(player_invs, ctx, item)
    return statement, gif
