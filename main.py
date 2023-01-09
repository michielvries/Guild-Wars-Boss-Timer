import discord
import asyncio
import message_handler

from constants import KEY

client = discord.Client(intents=discord.Intents.all())

with open("channels.txt", "r") as file:
    channels = file.read().split("\n")
    if len(channels[0]) == 0:
        channels = []


async def setup():
    client.loop.create_task(send_message())


client.setup_hook = setup


def add_channel(channel_id):
    # Deletes channel if it already existed
    delete_channel(channel_id)

    channels.append(str(channel_id))
    with open("channels.txt", "w") as file:
        text = "\n".join(channels)
        file.write(text)


def delete_channel(channel_id):
    for item in channels:
        if str(channel_id) in item:
            channels.remove(item)
    with open("channels.txt", "w") as file:
        text = "\n".join(channels)
        file.write(text)


@client.event
async def on_ready():
    text = "Logged in as: " + client.user.name
    print(text)
    print("".rjust(len(text), "_"))


@client.event
async def on_message(message):
    if message.content.startswith("/help"):
        channel_id = message.channel.id
        print(channel_id)
        await message.channel.send("Listens to `/addbosstimer` and `/removebosstimer`")

    elif message.content.startswith("/addbosstimer"):
        channel_id = message.channel.id
        if message.channel.type == discord.ChannelType.private:
            await message.channel.send("Try to use the `/addbosstimer` command on a server!")
            return
        add_channel(channel_id)
        await message.delete()
        notification = await message.channel.send("Added the boss timer, table will appear within 1 minute")
        await asyncio.sleep(10)
        try:
            await notification.delete()
        except discord.errors.NotFound:
            return

    elif message.content.startswith("/removebosstimer"):
        channel_id = message.channel.id
        delete_channel(channel_id)
        await message.channel.send("Removed the boss timer")


async def send_message():
    counter = 0
    while True:
        await client.wait_until_ready()

        if len(channels) != 0:
            counter += 1
            for data in channels:
                data = data.split(",")
                if len(data) == 1:
                    await send_new_message(data[0])
                elif len(data) == 2:
                    await modify_message(data[0], data[1])
                else:
                    print("Something went very wrong")

        await asyncio.sleep(10)


async def send_new_message(channel_id):
    channel = client.get_channel(int(channel_id))
    new_message = message_handler.get_message()
    message = await channel.send(new_message)
    message_id = message.id

    for idx, itm in enumerate(channels):
        if channel_id in itm:
            channels[idx] = f"{channel_id},{message_id}"

    with open("channels.txt", "w") as file:
        text = "\n".join(channels)
        file.write(text)


async def modify_message(channel_id, message_id):
    channel = client.get_channel(int(channel_id))
    if channel is None:
        delete_channel(channel_id)
        return None
    try:
        message = await channel.fetch_message(int(message_id))
    except discord.errors.NotFound:
        await send_new_message(channel_id)
        return

    new_message = message_handler.get_message()

    if message.content != new_message:
        print("VERNIEUWD")
        await message.edit(content=new_message)

client.run(KEY)
