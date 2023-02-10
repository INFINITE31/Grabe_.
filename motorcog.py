import asyncio
import motor
from motor import motor_asyncio
import os
from dotenv import load_dotenv
load_dotenv()
"""
This provides instances for the databases located in mongodb using motor (asynchronous version of pymongo)
"""

cluster3 = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("mongo"))
database3 = cluster3["infinite"]
votedb = database3["vote"]


cluster2 = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("mongo"))
database2 = cluster2["giveaways"]
gwdb = database2["giveaways"]


cluster4 = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("mongo"))
database4 = cluster4["afks"]
afkdb = database4["afks"]

cluster5 = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("afkdb"))
database5 = cluster5["infinite"]
reminderdb = database5["infinite"]


cluster6 = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("mongo"))
database6 = cluster6["tickets"]
ticketdb = database6["tickets"]


cluster7 = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("mongo"))
database7 = cluster7["bans"]
bandb = database7["bans"]


cluster8 = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("mongo"))
database8 = cluster8["automod"]
automod = database8["automod"]


cluster9 = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("mongo"))
database9 = cluster9["embed"]
embdb = database9["embed"]

cluster10 = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("mongo"))
database10 = cluster10["reroll"]
rolldb = database10["reroll"]

cluster11 = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("mongo"))
database11 = cluster11["timers"]
timerdb = database11["timers"]
