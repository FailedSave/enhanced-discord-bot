import discord
import game
import character
import json

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content.startswith('!join'):
            await game.join_game(message)

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

with open('.connections.json') as json_data:
    connections = json.load(json_data)

client = MyClient()
client.run(connections["PROD"])