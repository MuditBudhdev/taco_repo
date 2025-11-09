# quick summary
# all this code is doing is checking if the price on airline manager is below a certain value, if it is, 
# it sends a message in a discord server

import discord
import logging
from discord import app_commands

import asyncio



intents = discord.Intents.default()
client = discord.Client(intents=intents)


def function():   # everything else is just setup for the discord bot, the real fuel-checking code is here

    return True


async def check_function():

    await client.wait_until_ready()
    channel = await client.fetch_channel(CHANNEL_ID)
    while not client.is_closed():
        while True:
            if function():  
                await channel.send("the function returned true ")
                break 
            await asyncio.sleep(5)  

async def main():
    task = asyncio.create_task(check_function())
    await client.start(token)
    await task

asyncio.run(main())