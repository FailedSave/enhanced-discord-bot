import discord
import random
import json
import datetime
import character

active_games = {}
player_to_game = {}
channel_to_game = {}

stage_thresholds = [0, 35, 70, 105, 140]
#stage_thresholds = [0, 20, 40, 60, 80]
#stage_thresholds = [0, 10, 20, 30, 40]

class Game:
    def __init__(self, name: str, channel: discord.TextChannel):
        self.name = name
        self.players = []
        self.channel = channel
        self.started = False
        self.active_player = None
        self.scores = {}
        self.running_total = 0
        self.characters = {}
        self.stages = {}
        self.opponents = {}
        self.start_time = datetime.datetime.now()

    async def add_player(self, player: discord.Member):
        if len(self.players) >= 2:
            await self.channel.send(f"Game: {self.name} already has enough players")
            return
        self.players.append(player)
        self.scores[player] = 0
        self.stages[player] = -1
        await self.channel.send(f"{name_to_use(player)} has joined game {self.name}!")
        if len(self.players) == 2:
            (filename1, filename2) = character.choose_characters(self.players[0], self.players[1])
            self.characters[self.players[0]] = read_character(filename1)
            self.characters[self.players[1]] = read_character(filename2)
            self.opponents[self.players[0]] = self.players[1]
            self.opponents[self.players[1]] = self.players[0]
            message = f"{name_to_use(self.players[0])} is playing as **{self.characters[self.players[0]]['name']}**.\n"
            message += f"{name_to_use(self.players[1])} is playing as **{self.characters[self.players[1]]['name']}**.\n"
            await self.channel.send(message)
            await self.start()        
    
    async def start(self):
        self.active_player = random.choice(self.players)
        self.stages[self.active_player] = 0
        await self.display_stage(self.active_player, 0)
        await self.channel.send(f"Game: {self.name} is starting! The active player is **{name_to_use(self.active_player)}**")

    async def roll(self, player: discord.Member):
        if player != self.active_player:
            await self.channel.send(f"It's **{name_to_use(self.active_player)}'s** turn!")
            return
        die1 = random.randrange(1, 9)
        die2 = random.randrange(1, 9)
        if die1 == 1 or die2 == 1:
            summary = ("Bust!")
            self.running_total = 0
        else:
            self.running_total += die1 + die2
            summary = f"The running total is now **{self.running_total}**."
        await self.channel.send(f"The dice come up **{die1}** and **{die2}**. {summary}")
        if self.running_total == 0:
            await self.switch_turn()

    async def player_pass(self, player: discord.Member):
        if player != self.active_player:
            await self.channel.send(f"It's **{name_to_use(self.active_player)}'s** turn!")
            return
        self.scores[player] += self.running_total
        await self.channel.send(f"Banking **{self.running_total}** points. {name_to_use(player)}'s score is now **{self.scores[player]}**.")
        self.running_total = 0
        while (self.scores[player] > stage_thresholds[self.stages[player] + 1]):
            self.stages[player] += 1
            await self.display_stage(self.opponents[player], self.stages[player])
            if (self.stages[player] == len(stage_thresholds) - 1):
                break
        if await self.check_game_end(player):
            return
        await self.switch_turn()

    async def display_stage(self, player: discord.Member, stage_num):
        selection = random.choice(self.characters[player]["stages"][stage_num])
        image = discord.Embed(url=selection["url"]) 
        image.set_image(url=selection["url"])
        await self.channel.send(selection["description"], embed=image)

    async def announce_active_player(self):
        await self.channel.send(f"It is now **{name_to_use(self.active_player)}'s** turn.")
        if self.stages[self.active_player] == -1:
            self.stages[self.active_player] = 0
            await self.display_stage(self.active_player, 0)

    async def switch_turn(self):
        self.active_player = self.opponents[self.active_player]
        await self.announce_active_player()

    async def check_game_end(self, player: discord.Member):
        if (self.stages[player] == len(stage_thresholds) - 1):
            await self.channel.send(f"The game is over! **{name_to_use(self.active_player)}** is the winner!")
            await self.channel.send(f"Thanks for playing! Art by **ColorfulTrick**; programming by **FailedSave**")
            self.end_game()
            return True
        return False

    def end_game(self):
        for player in self.players:
            del player_to_game[player]
        del active_games[self.name]
        del channel_to_game[self.channel]

def read_character(filename: str):
    with open(f"{filename}.json") as json_data:
        return json.load(json_data)

async def join_game(message: discord.Message):
    words = message.content.split(None, 1)
    if len(words) != 2:
        await message.channel.send(f"Usage: !join <gamename>")
    name = words[1]
    player = message.author
    if player in player_to_game:
        await message.channel.send(f"{name_to_use(player)} is already in a game.")
        return

    if name not in active_games:
        if message.channel in channel_to_game:
            # If the game has expired, remove it. Otherwise, prevent this.
            delta = datetime.datetime.now() - channel_to_game[message.channel].start_time
            if delta > datetime.timedelta(minutes = 20):
                channel_to_game[message.channel].end_game()
            else:
                await message.channel.send(f"There is already a game in progress on this channel.")
                return
        active_games[name] = Game(name, message.channel)
        channel_to_game[message.channel] = active_games[name] 
        await message.channel.send(f"Creating game: {name}")
    player = message.author
    player_to_game[player] = active_games[name]
    await active_games[name].add_player(player)

async def add_player_to_game(message: discord.Message, player: discord.Member, game):
    if game not in active_games:
        raise f"Game {game} unexpectedly not found" 
    if len(active_games[game].players) >= 2:
        await message.channel.send(f"Game: {game} already has enough players")
        return
    active_games[game].players.append(player)
    player_to_game[player] = game
    await message.channel.send(f"{name_to_use(player)} has joined game {game}!")

async def player_roll(message: discord.Message):
    if message.author not in player_to_game:
        await message.channel.send(f"{name_to_use(message.author)} is not in a game yet.")
        return
    await player_to_game[message.author].roll(message.author)

async def player_pass(message: discord.Message):
    if message.author not in player_to_game:
        await message.channel.send(f"{name_to_use(player)} is not in a game yet.")
        return
    await player_to_game[message.author].player_pass(message.author)    

def name_to_use(player: discord.Member):
    if player.nick != None:
        return player.nick
    return player.name

