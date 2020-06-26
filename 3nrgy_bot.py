import discord
import os
import random
import datetime
from boto.s3.connection import S3Connection
import pytz
from dotenv import load_dotenv
from pytz import timezone
from discord.ext import commands #discord extension

#load_dotenv() # make .env file accessible
#token = os.getenv("BOT_TOKEN") ---if you want to run locally

token = os.environ.get("BOT_TOKEN") # discord bot token goes here
client = commands.Bot(command_prefix = '//') #bot instance created, called client
'''
@client.event #function represents event (1st event)
async def on_ready(ctx): #asynchronous function - when bot is ready (first event)
    print("I'm ready, now!")
    await ctx.send("I'm ready!")
'''

# trading system command_prefix
player_invs = {}

@client.command(description = "start a new inventory to start trading")
async def new_inv(ctx):
    global player_invs # call global var
    person = ctx.author
    if player_invs.get(person) == None: # if player does not have an inv
        player_invs.update({person:[]})
        await ctx.send("New inventory initialised. \n You're all set.")
    else:
        await ctx.send("You already have an inventory. If you want to reset, use the reset command.")

@client.command(description = "view inventory")
async def see_inv(ctx):
    global player_invs
    person = ctx.author
    if player_invs.get(person) != None:
        await ctx.send("Looking through your inventory...")
        if len(player_invs[person]) != 0:
            for i in player_invs[person]:
                await ctx.send(i.upper())  # cannot send multiple vars at once
        else:
            await ctx.send("You have nothing atm.")
    else:
        await ctx.send("You do not have an inventory yet. Use 'new_inv' command to make one.")

@client.command(description="testing - add item to inv")
async def add(ctx): # add check to see if inv is real
    global player_invs
    person = ctx.author
    person_inv = player_invs[person]
    person_inv.append("starter")
    player_invs[person] = person_inv
    await ctx.send("Starter item added.")

@client.command(description="start a trade")
async def ask_trade(ctx, recipient, skin, trade_skin):
    global player_invs
    person = ctx.author
    await ctx.send(person)
    await ctx.send(recipient)
    await ctx.send(skin)
    await ctx.send(trade_skin)
    await ctx.send(player_invs)
    await ctx.send(player_invs[person])
    await ctx.send(player_invs[recipient])
    person_inv = player_invs[person]
    recipient_inv = player[recipient]
    await ctx.send("Checking skins...")
    if skin in person_inv and trade_skin in recipient_inv: #if they actually have skins, proceed
        await ctx.send(recipient.mention()+ " do you want to trade" + skin + "for your" + trade_skin + "? (from{})".format(person))
    else:
        await ctx.send("That is an invalid trade - check both of you have those skins.")
# view inv command
# roulette command
#reset inv command
#trade command
#view others' invs command

@client.command(description = "tells you the bot's ping")
async def ping(ctx): #ctx is context
    person = ctx.author
    await ctx.send(f'Pong! {round(client.latency * 1000, 2)}ms')

@client.command(aliases = ['8ball', 'eightball'], description = "ask the virtual 8ball (always correct)") #setting other ways to invoke command
async def _8ball(ctx, *, question): #asterisk allows multiple arguments as one
    responses = ['It is certain.', 'Definitely.', 'Never in your life.', 'Maybe.', 'Probably not.']
    await ctx.send(f'Question: {question}\n Answer: {random.choice(responses)}')

@client.command(aliases = ['Hello', 'hi', 'Hi', 'hey', 'Hey'], description = "says hello")
async def hello(ctx):
    greetings = ['Hello there!', 'wassup', 'Yolo.', 'Ayyyy my guy.', 'Why are you trying to talk to me? \n jkkkkkk']
    await ctx.send(random.choice(greetings))

@client.command(aliases = ['how_are_you', 'how_are_you?', 'Howareyou'], description = "tells you how it's feeling")
async def howareyou(ctx):
    replies = ['A bit sad,', 'Ok, I guess,', 'Good,', 'Really happy,', "Don't bother me - I'm doing Karthik's Maths homework. Why do you think he does that well?", 'I feel human.']
    name = str(ctx.author)
    name = str(name[:-5])
    randreply = random.choice(replies)
    if randreply == replies[4]:
        randreply = "Don't bother me - you know for well that I'm doing your Homework,"
    await ctx.send(randreply + ' ' + name)

@client.command(description = "tells you the date")
async def date(ctx):
    full_date = ""
    info = datetime.datetime.now()
    day_of_week = info.strftime("%a")
    day_num = info.strftime("%d")
    month = info.strftime("%b")

    if day_num[-1] == 1 and day_num != 11:
        day_num = day_num + "st"
    elif day_num[-1] == 2:
        day_num = day_num + "nd"
    elif day_num[-1] == 3:
        day_num = day_num + "rd"
    else:
        day_num = day_num + "th"

    full_date = day_of_week + " the " + day_num + " of " + month
    await ctx.send(full_date)

@client.command(description = "tells you the time right now")
async def time(ctx):
    full_time = ""
    tz = pytz.timezone('GB')
    fullinfo = datetime.datetime.now(tz)
    time = str(fullinfo)[11:16]
    await ctx.send("It's " + time)

client.run(token) #run client
