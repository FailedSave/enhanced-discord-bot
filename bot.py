import discord
import game
import character
import asyncio
import fate
from setting_storage import settings_from_user_id, target_settings_from_user_id
import setting_storage
import stats_storage
import stats
import settings
import json
import help
from settings import Settings

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        setting_storage.load_settings()
        stats_storage.load_stats()

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content.startswith('!join'):
            await game.join_game(message)
        
        if message.content.startswith('!leave'):
            await game.leave_game(message)

        if message.content.startswith('!char'):
            await character.handle_char(message)

        if message.content == '!quit':
            if message.author.id != 261495649327906816:
                return
            await message.channel.send('shutting down')
            await self.close()

        if message.content == '!roll':
            await game.player_roll(message)
        
        if message.content == '!pass' or message.content == '!bank':
            await game.player_pass(message)

        if message.content.startswith('!helpless'):
            await settings.handle_helpless(client, message, message.author.name, message.channel, settings_from_user_id(message.author))
        elif message.content.startswith('!h'):
            await help.handle_help(client, message, message.author.name, message.channel, settings_from_user_id(message.author))

        if message.content.startswith('!fate'):
            await fate.handle_fate(client, message, message.author.name, message.channel, settings_from_user_id(message.author))

        if message.content.startswith('!set'):
            await settings.handle_set(client, message, message.author.name, message.channel, settings_from_user_id(message.author))

        if message.content.startswith('!viewsettings'):
            await settings.handle_view_settings(client, message, message.author.name, message.channel, settings_from_user_id(message.author))

        if message.content.startswith('!tfate'):
            await fate.handle_target_fate(client, message, message.author.name, message.channel, target_settings_from_user_id(message.author))

        if message.content.startswith('!tset'):
            await settings.handle_set(client, message, message.author.name, message.channel, target_settings_from_user_id(message.author))

        if message.content.startswith('!tviewsettings'):
            await settings.handle_view_settings(client, message, message.author.name, message.channel, target_settings_from_user_id(message.author))

        if message.content.startswith('!stats'):
            await stats.handle_view_stats(client, message, message.author.name, message.channel)

        if message.content.startswith('!save'):
            await setting_storage.save_settings()

        if message.content.startswith('!wfate'):
            await fate.handle_whisper_fate(client, message, message.author.name, message.channel, target_settings_from_user_id(message.author))            

with open('.connections.json') as json_data:
    connections = json.load(json_data)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

async def autosave_task():
    await client.wait_until_ready()
    while not client.is_closed():
        await asyncio.sleep(300)
        await setting_storage.save_settings()
        await stats_storage.save_stats()

client.run(connections["MAIN"])