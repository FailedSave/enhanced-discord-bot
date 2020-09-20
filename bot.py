import discord
import game
import character

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

        if message.content == 'ping':
            image = discord.Embed(url="https://cdn.discordapp.com/attachments/514279423688835087/734630064078979072/Liz_Level2_Pose1_Camera_1.png") 
            image.set_image(url="https://cdn.discordapp.com/attachments/514279423688835087/734630064078979072/Liz_Level2_Pose1_Camera_1.png")
            await message.channel.send('pong')
            await message.channel.send(embed=image)

        if message.content == '!quit':
            await message.channel.send('shutting down')
            await self.close()

        if message.content == '!roll':
            await game.player_roll(message)
        
        if message.content == '!pass' or message.content == '!bank':
            await game.player_pass(message)

with open('.connections.json') as json_data:
    connections = json.load(json_data)

client = MyClient()
client.run(connections["MAIN"])