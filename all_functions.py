import discord
import random
import discord
import os
import random
import datetime
import pytz
#from dotenv import load_dotenv -- for local
from pytz import timezone
from discord.ext import commands #discord extension
from all_functions import *
import asyncpg
import psycopg2

'''
def add_specified_to_inv(player_invs, ctx, item):
    person = str(ctx.author.id)
    person_inv = player_invs[person]
    person_inv.append(item)
    player_invs[person] = person_inv
    return "item added."

def read_inv(ctx, player_invs, person):
    if person != None: #if person variable is provided
        person = str(person.id)
    else:
        person = str(ctx.author.id)
    if player_invs.get(person) != None:  #get_inv_query = "select user_inv from user_info WHERE user_id = '&s' " % person; cursor.execute(user_inv_query); person_inv = cursor.fetchall()
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
'''

def create_new_inventory_db(ctx):
    person = str(ctx.author.id)
    # check if person has inventory
    result = query_manage("insert into user_info (user_id, user_inv) VALUES ('{}', '{}')".format(person, {}))
    if result != 0:
        return "New inventory created."
    return "Error - do you already have an inventory?"

def read_inv_db(person): #read inventory of any specified person as an optional parameter
    result = query_manage("select user_inv from user_info WHERE user_id = '{}'".format(person))
    if result != 0 and result != []: # result is [] when the table is empty
        person_inv = ', '.join(result[0][0])
        if len(person_inv) > 0:
            return person_inv
        return "" #"You have nothing atm."
    return 0 #"Error - do you have an inventory?"

def add_item_to_inv_db(ctx, item):
    person = str(ctx.author.id)
    if read_inv_db(person) != 0:
        result = query_manage("update user_info SET user_inv[CARDINALITY(user_inv)+1] = '{}' where user_id = '{}'".format(item, person))
        if result != 0:
            return 1
        return 0
    return 0

def get_item(list_name):
    item = list_name[random.randint(0, len(list_name)-1)] #-1 because indexing starts with 0
    return item

def spin_roulette_db(ctx):
    randnum = random.randint(0, 100)
    if randnum > 60:
        uncommon_list = ["aqua", "bark_auto", "blushed_mma", "carbon_mmr", "commo", "digital_auto", "dropper"]
        #item = "uncommon"
        item = get_item(uncommon_list)
        gif = 'uncommon.gif'
        statement = "You got " + item #make it display different gifs
    elif 30 < randnum <= 60:
        rare_list = ["artic_auto", "auto_machinist", "autumn_auto", "bloodripper", "flecken_auto", "hazard_auto", "jade", "kodac_auto"]
        #item = "rare"
        item = get_item(rare_list)
        gif = 'rare.gif'
        statement = "You got " + item
    elif 15 < randnum <= 30:
        epic_list = ["black_ice", "barbed_auto", "blaze_auto", "m14_chartreuse", "mma_cygento", "mma_octo"]
        #item = "epic"
        item = get_item(epic_list)
        gif = 'epic.gif'
        statement = "You span " + item
    elif 7 < randnum <= 15:
        legendary_list = ["magnis", "shot_element", "acid_breath", "101_skullbreaker", "haste", "lava_bolt"]
        #item = "legendary"
        item = get_item(legendary_list)
        gif = 'legendary.gif'
        statement = "Legendary " + item + "!"
    elif 3 < randnum <= 7:
        relic_list = ["mma_plasma", "neuromance", "awp_pacemaker", "awp_stream", "neon_reaver", "razor"]
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
    result = add_item_to_inv_db(ctx, item)
    print(result)
    if result == 1:
        return statement, gif
    return "Error, not able to add item."

def ask_for_trade_db(ctx, recipient, skin, trade_skin):
    person, recipient_name, recipient = str(ctx.author.id), str(recipient), str(recipient.id)
    #if person != recipient and inv_check(person)==1 and inv_check(recipient)==1: # (if trade already a thing)if person isn't recipient, if they have invs, then if they have skins

    if person == recipient:
        return "You can't trade with yourself. Lol."

    person_inv, recipient_inv = read_inv_db(person), read_inv_db(recipient)
    if person_inv == 0 or recipient_inv == 0:
        return "Check if you both have inventories."
    if skin not in person_inv or trade_skin not in recipient_inv: # check this
        return "Check both of you have the skins you want to trade."
    if skin == "" or trade_skin == "":
        return "You can't trade nothing."
    # if trade already available:
    #   return "Trade already pending."
    # select * from ongoing_trades where ((person = 'PERSON_ID' and recipient = 'RECIPIENT_ID') or (person = 'RECIPIENT_ID' and recipient = 'PERSON_ID')) and ((skin = 'SKIN' and trade_skin = 'TRADE_SKIN') or (skin='TRADE_SKIN' and trade_skin='SKIN'))
    check_for_dup = query_manage("select * from ongoing_trades where ((person = '{}' and recipient = '{}') or (person = '{}' and recipient = '{}')) and ((skin = '{}' and trade_skin = '{}') or (skin='{}' and trade_skin='{}'))".format(person, recipient, recipient, person, skin, trade_skin, trade_skin, skin))
    print('dup_check = ', check_for_dup)
    if check_for_dup != 1 or check_for_dup!=[]:
        return "This trade is already a pending trade."
    add_trade_to_db = query_manage("insert into ongoing_trades (person, recipient, skin, trade_skin) VALUES ('{}', '{}', '{}', '{}')".format(person, recipient, skin, trade_skin))
    if add_trade_to_db == 1:
        return "When " + recipient_name + " accepts the trade, the items will be swapped."
    else:
        return "Error. Trade was valid but trade was not able to be added to database."


def ask_user_for_trade(player_invs, ctx, ongoing_trades, recipient, skin, trade_skin):
    person, recipient_name, recipient = str(ctx.author.id), str(recipient), str(recipient.id) # person is ALWAYS PERSON WHO STARTS TRADE
    trade = [person, recipient, skin, trade_skin] #always this TRADE STRUCTURE
    if player_invs.get(person) and player_invs.get(recipient)!= None: #make this into check_validity function
        person_inv, recipient_inv = player_invs[person], player_invs[recipient]
    else:
        return "Missing inventories."
    if skin in person_inv and trade_skin in recipient_inv and person!=recipient: #if they actually have skins, proceed, ADD check if trade already thing
        ongoing_trades.append(trade)
        return "When " + recipient_name + " accepts the trade, the items will swap."
    else:
        return "That is an invalid trade."

def execute_trade(ctx, player_invs, ongoing_trades, starter, trade_skin, skin):
    person = str(ctx.author.id)
    starter = str(starter.id)
    if player_invs.get(person) and player_invs.get(recipient)!= None:
        person_inv, recipient_inv = player_invs[person], player_invs[recipient]
    else:
        return "Missing inventories."
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

def spin_roulette(ctx, player_invs):
    randnum = random.randint(0, 100)
    if randnum > 60:
        uncommon_list = ["aqua", "bark_auto", "blushed_mma", "carbon_mmr", "commo", "digital_auto", "dropper"]
        #item = "uncommon"
        item = get_item(uncommon_list)
        gif = 'uncommon.gif'
        statement = "You got " + item #make it display different gifs
    elif 30 < randnum <= 60:
        rare_list = ["artic_auto", "auto_machinist", "autumn_auto", "bloodripper", "flecken_auto", "hazard_auto", "jade", "kodac_auto"]
        #item = "rare"
        item = get_item(rare_list)
        gif = 'rare.gif'
        statement = "You got " + item
    elif 15 < randnum <= 30:
        epic_list = ["black_ice", "barbed_auto", "blaze_auto", "m14_chartreuse", "mma_cygento", "mma_octo"]
        #item = "epic"
        item = get_item(epic_list)
        gif = 'epic.gif'
        statement = "You span " + item
    elif 7 < randnum <= 15:
        legendary_list = ["magnis", "shot_element", "acid_breath", "101_skullbreaker", "haste", "lava_bolt"]
        #item = "legendary"
        item = get_item(legendary_list)
        gif = 'legendary.gif'
        statement = "Legendary " + item + "!"
    elif 3 < randnum <= 7:
        relic_list = ["mma_plasma", "neuromance", "awp_pacemaker", "awp_stream", "neon_reaver", "razor"]
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

def check_trades(ctx, player_invs, ongoing_trades):
    user = str(ctx.author.id)
    display_list = []
    if player_invs.get(user) != None:
        for trade in ongoing_trades:
            if trade[0] == user or trade[1] == user:
                display_list.append(trade)
                print(trade)
        if len(display_list) > 0:
            return ', '.join(map(str,display_list)) #converts each element to string so that it can be join()
        else:
            return "No ongoing trades involving you."
    else:
        return "No inventory."

def embed_it(ctx, the_value):
    embed = discord.Embed(color = 0x61cc33)
    embed.add_field(name=str(ctx.author),value=the_value)
    return embed

def query_manage(the_query): # handles queries
    DATABASE_URL = os.environ['DATABASE_URL']
    con = psycopg2.connect(DATABASE_URL, sslmode = 'require')
    cursor = con.cursor() #used to execute commands like a mouse cursor is used to click things
    try:
        cursor.execute(the_query)
        try:
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(e) # see what exception happened
            return 1 #query was carried out
        finally:
            con.commit()
    except:
        return 0
    finally:
        con.close()
