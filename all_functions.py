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

# ----- FOR I IN PEOPLE WITH INVS, set_refresh_for(i)

def redeploy_refresh():
    a = query_manage("select user_id from user_info")
    print(a)
    if (isinstance(a, list)):
        i = 0
        list1 = []
        while i < len(a):
            user = a[i][0]
            print('redeploy_refresh for ', user)
            list1.append(user)
            i+=1

        print(list1)
        for i in list1:
            set_refresh_for(i)
    #for i in users: set_refresh_for(person)

def create_new_inventory_db(ctx):
    person = str(ctx.author.id)
    # check if person has inventory
    result = query_manage("insert into user_info (user_id, user_inv) VALUES (%s, '{}')", (person,))
    if result != 0:
        set_refresh_for(person) # set refresh --- CHANGE BECAUSE NEW DEPLOYS WON'T REALISE
        return "New inventory created."
    return "Error - do you already have an inventory?"

def read_inv_db(person): #read inventory of any specified person as an optional parameter
    result = query_manage("select user_inv from user_info WHERE user_id = %s", (person,))
    if result != 0 and result != []: # result is [] when the table is empty
        person_inv = ', '.join(result[0][0])
        if len(person_inv) > 0:
            return person_inv
        return "" #"You have nothing atm."
    return 0 #"Error - do you have an inventory?"

def get_num_of_spins(person):
    result = query_manage("select num_of_spins from user_info where user_id = %s", (person,))
    return result

def add_item_to_inv_db(person, item):
    if read_inv_db(person) != 0:
        result = query_manage("update user_info SET user_inv[CARDINALITY(user_inv)+1] = %s where user_id = %s", (item, person))
        if result != 0:
            return 1
        return 0
    return 0

def get_item(list_name):
    item = list_name[random.randint(0, len(list_name)-1)] #-1 because indexing starts with 0
    return item

def decrease_spin_num(person):
    result = query_manage("update user_info set num_of_spins = num_of_spins - 1 where user_id = %s", (person,))
    if result != 0:
        return 1
    return 0

def give_3_spins(person):
    if read_inv_db(person)!= 0:
        result = query_manage("update user_info set num_of_spins = num_of_spins + 3 where user_id = %s", (person,))
        if result == 1:
            return 1
        return 0
    return 0

def get_datetime():
    #No timezone
    return_ = datetime.datetime.now()
    return return_

def refresh_time_left(person):
    result = query_manage("select refresh_time from user_info where user_id = %s", (person,))
    start_time = datetime.datetime.strptime(result[0][0], '%Y-%m-%d %H:%M:%S.%f')

    ### ADD 6 hours to start refresh time
    end_time = start_time + datetime.timedelta(hours=6)
    time = get_datetime()
    return_ = str(end_time - time)
    return_ = return_[:7]
    return return_

# ----    REFRESH TIMER
import threading
def timer(id):
    print('alarm set for ', id)
    timer2 = threading.Timer(21600, handler, [id])
    timer2.start()
    time = get_datetime()
    result = query_manage("update user_info set refresh_time = %s", (time,))
#10800
def handler(c): # handles the alarm
    print('alarm received for ', c)
    print(c)
    #print(type(c))
    result = give_3_spins(c)
    if result == 0:
        print('refresh cancelled - error occured with ', c)
        return #LEAVE LOOP
    timer(c)

def set_refresh_for(a):
    timer(a)
# -----

def spin_roulette_db(ctx):
    person = str(ctx.author.id)
    if read_inv_db(person) == 0:
        return "You don't have an inventory, yet. Make one. (//help if you're unsure of what to do)"
    check_spins = get_num_of_spins(person)[0][0]
    if check_spins <= 0:
        return "You don't have enough spins."
    randnum = random.randint(0, 100)
    if randnum > 60:
        uncommon_list = ["aqua", "bark_auto", "blushed_mma", "carbon_mmr", "commo", "digital_auto", "dropper"]
        item = get_item(uncommon_list)
        #gif = 'uncommon.gif'
        rarity = 'uncommon'
        #statement = "You got " + item
    elif 30 < randnum <= 60:
        rare_list = ["artic_auto", "auto_machinist", "autumn_auto", "bloodripper", "flecken_auto", "hazard_auto", "jade", "kodac_auto"]
        item = get_item(rare_list)
        #gif = 'rare.gif'
        rarity = 'rare'
        #statement = "You got " + item
    elif 15 < randnum <= 30:
        epic_list = ["black_ice", "barbed_auto", "blaze_auto", "m14_chartreuse", "mma_cygento", "mma_octo"]
        item = get_item(epic_list)
        #gif = 'epic.gif'
        rarity = 'epic'
        #statement = "You span " + item
    elif 7 < randnum <= 15:
        legendary_list = ["magnis", "shot_element", "acid_breath", "101_skullbreaker", "haste", "lava_bolt"]
        item = get_item(legendary_list)
        #gif = 'legendary.gif'
        rarity = 'legendary'
        #statement = "Legendary " + item + "!"
    elif 3 < randnum <= 7:
        relic_list = ["mma_plasma", "neuromance", "awp_pacemaker", "awp_stream", "neon_reaver", "razor"]
        item = get_item(relic_list)
        #gif = 'relic.gif'
        rarity = 'relic'
        #statement = "Nice, you got relic - " + item
    elif 1 < randnum <= 3:
        contraband_list = ["raynb0w", "1ad-da0", "xon-vox", "exos", "futuristic", "izula", "hackusate", "pellucid"]
        item = get_item(contraband_list)
        #gif = 'contraband.gif'
        rarity = 'contraband'
        #statement = "You got " + item
    else:
        unobtainable_list = ["disintegrator", "anti-matter", "wutdatime_exclusive"]
        item = get_item(unobtainable_list)
        #gif = 'unobtainable.gif'
        rarity = 'unobtainable'
        #statement = "Wow. Unobtainable - " + item
    result = add_item_to_inv_db(person, item)
    result2 = decrease_spin_num(person)
    print(result)
    if result == 1 and result2 == 1:
        skin_image = '%s.png'%item
        #return statement, gif, skin_image
        skin_embed = embed_roulette(item, skin_image, rarity)
        return skin_embed
    elif result2 == 0:
        return "Not able to decrease the number of roulette spins, but item added."
    return "Error, not able to add item."

def any_dup(person1, person2, skin, trade_skin): #person1 = author
    check_for_dup = query_manage("select * from ongoing_trades where ((person = %s and recipient = %s) or (person = %s and recipient = %s)) and ((skin = %s and trade_skin = %s) or (skin=%s and trade_skin=%s))",(person1, person2, person2, person1, skin, trade_skin, trade_skin, skin))
    if check_for_dup != 1 and check_for_dup!=[]:
        return 1 # there are dupes
    return 0 # no dupes

def already_trade(person, starter, skin, trade_skin):
    result = query_manage("select * from ongoing_trades where person = %s and recipient = %s and skin=%s and trade_skin=%s ",(starter, person, trade_skin, skin))
    if result != 1 and result != []:
        return 1
    return 0

def ask_for_trade_db(ctx, recipient, skin, trade_skin):
    person, recipient_name, recipient = str(ctx.author.id), str(recipient), str(recipient.id)

    if person == recipient:
        return "You can't trade with yourself. Lol."

    person_inv, recipient_inv = read_inv_db(person), read_inv_db(recipient)
    if person_inv == 0 or recipient_inv == 0:
        return "Check if you both have inventories."
    if skin not in person_inv or trade_skin not in recipient_inv: # check this
        return "Check both of you have the skins you want to trade."
    if skin == "" or trade_skin == "":
        return "You can't trade nothing."

    dup_check = any_dup(person, recipient, skin, trade_skin)
    if dup_check == 1:
        return "This trade is already a pending trade."

    add_trade_to_db = query_manage("insert into ongoing_trades (person, recipient, skin, trade_skin) VALUES (%s, %s, %s, %s)",(person, recipient, skin, trade_skin))
    if add_trade_to_db == 1:
        return "When " + recipient_name + " accepts the trade, the items will be swapped."
    else:
        return "Error. Trade was valid but trade was not able to be added to database."

def accept_trade(ctx, starter, skin, trade_skin):
    person, starter_name, starter = str(ctx.author.id), str(starter), str(starter.id)
    trade_check = already_trade(person, starter, skin, trade_skin)
    print(trade_check)

    if trade_check == 1: # if trade already in ongoing_trades
        person_inv, starter_inv = read_inv_db(person), read_inv_db(starter)
        if skin in person_inv and trade_skin in starter_inv:
            result1 = query_manage("update user_info SET user_inv = array_replace(user_inv, %s, %s) where user_id = %s",(trade_skin, skin, starter))
            result2 = query_manage("update user_info SET user_inv = array_replace(user_inv, %s, %s) where user_id = %s",(skin, trade_skin, person))
            print(result1, result2)
            if result1 != 0 and result2 != 0:
                result3 = query_manage("delete from ongoing_trades where person = %s and recipient = %s and skin=%s and trade_skin=%s",(starter, person, trade_skin, skin)) # delete from ongoing_trades
                if result3 != 3:
                    return "Trade with " + starter_name + " was complete."
                return "Error. Unable to delete from ongoing_trades."
            return "Error. Unable to add and remove items from inventories."
        return "Skins not in invs anymore."
    return "You can't accept a trade that hasn't been requested."

def my_trades(ctx, client):
    user = str(ctx.author.id)
    result = query_manage("select * from ongoing_trades where person = %s or recipient = %s",(user, user))
    print(result)
    print(type(result))
    if result == []:
        return "No trades."

    a = result
    for i in a:
        index = a.index(i)
        i = list(i)
        print(i)
        a[index]= i

    i = 0
    for i in range(0, len(a)):
        b = int((a[i][0]))
        user = str(client.get_user(b))
        a[i][0] = user
        i +=1

    i = 0
    for i in range(0, len(a)):
        b = int((a[i][1]))
        user =str(client.get_user(b))
        print(user)
        a[i][1] = user
        i+=1

    b = a

    return_ = ''
    a = -1
    print("\n")
    for i in b:
        a +=1
        for i in b[a]:
            return_ = return_ + i + " "
            a += 1
        return_ = return_ + "\n"
        a = 0

    print(return_)

    return return_
    #return result

def embed_it(ctx, the_value):
    embed = discord.Embed(color = 0x61cc33)
    embed.add_field(name=str(ctx.author),value=the_value)
    return embed

def embed_roulette(skin_name, skin_image, rarity):
    embed = discord.Embed(color = 0x61cc33, title = skin_name) # change color depending on rarity
    embed.set_image(url='attachment://%s'%skin_image)
    embed.add_field(name='Rarity:', value=rarity)
    return embed

def query_manage(the_query, data=None): # handles queries   ---- MOVE TO TOP
    DATABASE_URL = os.environ['DATABASE_URL']
    con = psycopg2.connect(DATABASE_URL, sslmode = 'require')
    cursor = con.cursor() #used to execute commands like a mouse cursor is used to click things
    try:
        if data==None:
            cursor.execute(the_query)
        else:
            cursor.execute(the_query, data)
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
