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
import threading
#------MOVE ALL IMPORTS + VARS INTO ALL_FUNCTIONS

#load_dotenv() # make .env file accessible
#token = os.getenv("BOT_TOKEN") ---if you want to run locally

token = os.environ.get("BOT_TOKEN") # discord bot token goes here#
client = commands.Bot(command_prefix = '//') #bot instance created, called client

DATABASE_URL = os.environ['DATABASE_URL']

@client.event #function represents event (1st event)
async def on_ready(): #asynchronous function - when bot is ready (first event)
    print("I'm ready, now!")

#reset inv command
#make check_trades return statement more userfriendly
#add avatar to embeds
#tier list
#make a check validity cmd

@client.command(description = "tells you the bot's ping")
async def ping(ctx):
    await ctx.send(embed=embed_it(ctx, f'Pong! {round(client.latency * 1000, 2)}ms'))

@client.command(aliases = ['8ball', 'eightball'], description = "ask the virtual 8ball (always correct)") #setting other ways to invoke command
async def _8ball(ctx, *, question): #asterisk allows multiple arguments as one
    responses = ['It is certain.', 'Definitely.', 'Never in your life.', 'Maybe.', 'Probably not.']
    await ctx.send(embed=embed_it(ctx, f'Question: {question}\n Answer: {random.choice(responses)}'))

@client.command(aliases = ['Hello', 'hi', 'Hi', 'hey', 'Hey'], description = "says hello")
async def hello(ctx):
    greetings = ['Hello there!', 'wassup', 'Yolo.', 'Ayyyy my guy.', 'Why are you trying to talk to me? \n jkkkkkk']
    await ctx.send(embed=embed_it(ctx, random.choice(greetings)))

@client.command(aliases = ['how_are_you', 'how_are_you?', 'Howareyou'], description = "tells you how it's feeling")
async def howareyou(ctx):
    replies = ['A bit sad,', 'Ok, I guess,', 'Good,', 'Really happy,', "Don't bother me - I'm doing Karthik's Maths homework. Why do you think he does that well?", 'I feel human.']
    name = str(ctx.author)
    randreply = random.choice(replies)
    if randreply == replies[4]:
        randreply = "Don't bother me - you know for well that I'm doing your Homework,"
    await ctx.send(embed=embed_it(ctx, randreply + ' ' + name))

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
    await ctx.send(embed=embed_it(ctx, full_date))

@client.command(description = "tells you the time right now")
async def time(ctx):
    full_time = ""
    tz = pytz.timezone('GB')
    fullinfo = datetime.datetime.now(tz)
    time = str(fullinfo)[11:16]
    await ctx.send(embed=embed_it(ctx, "It's " + time))

# ------ trading system cmds
@client.command()
async def make_inv(ctx):
    await ctx.send(embed=embed_it(ctx, create_new_inventory_db(ctx)))

@client.command()
async def see_inv(ctx, person:discord.Member=None):
    #await ctx.send(embed=embed_it(ctx, read_inv_db(ctx)))
    if person != None:
        person = str(person.id)
    else:
        person = str(ctx.author.id)
    result = read_inv_db(person)
    if result == 0:
        statement = "Error - do you have an inventory?"
    elif result == "":
        statement = "You have nothing atm."
    else:
        statement = result
    await ctx.send(embed=embed_it(ctx, statement))

@client.command(description="use a spin on the roulette")
async def roulette(ctx):
    result = spin_roulette_db(ctx)
    if len(result) == 2:
        await ctx.send(embed=embed_it(ctx, result[0]))
        await ctx.send(file=discord.File(result[1]))
    else:
        await ctx.send(embed=embed_it(ctx, result))

@client.command(description="ask someone for a trade (trade structure is: the_recipient/other_person, your_skin, their_skin - even when you accept).")
async def ask_trade(ctx, recipient:discord.Member, skin, trade_skin):
    await ctx.send(embed=embed_it(ctx, ask_for_trade_db(ctx, recipient, skin, trade_skin)))
#insert into ongoing_trades (person, recipient, skin, trade_skin) VALUES ('test2', 'recipient_id2', 'aqua_ski2n', 'commo_trade_ski2n')  -- trades

@client.command(description="accept a trade (trade structure is: starter of trade/the other person, your_skin, their_skin).")
async def yes_trade(ctx, starter:discord.Member, skin, trade_skin):
    await ctx.send(embed=embed_it(ctx, accept_trade(ctx, starter, skin, trade_skin)))

@client.command(description="check which pending trades you're involved in")
async def any_trades(ctx):
    await ctx.send(embed=embed_it(ctx, my_trades(ctx)))

#    ---- - - -- - --- CHANGE .FORMAT TO %s TO PREVENT SQL INJECTION
redeploy_refresh()
client.run(token) #run client
