import discord
import random

class Character:
    def __init__(self, name, description, filenames):
        self.name = name
        self.description = description
        self.filenames = filenames

player_to_preferred_character = {}

characters = []
characters.append(Character("None", "Invalid Character", []))
characters.append(Character("Liz Harper", "Liz Harper (Scientist)", ["liz_stone", "liz_plastic"]))
characters.append(Character("Josephiend Pye", "Josephiend Pye (Magician)", ["josie_stone", "josie_silver", "josie_gold", "josie_plastic"]))

async def handle_char(message: discord.Message):
    words = message.content.split(None, 1)
    if len(words) == 1:
        await list_characters(message)
    elif len(words) != 2:
        await message.channel.send(f"Usage: !char or !char <number>")
    else:
        await pick_preferred_character(message, words[1])

async def list_characters(message: discord.Message):
    ix = 1
    text = "\n**List of Available Characters:**\n"
    for character in characters:
        if character.name == "None":
            continue
        text += f"{ix}. {character.description}\n"
        ix += 1
    await message.channel.send(text)

async def pick_preferred_character(message: discord.Message, choice_str):
    player = message.author
    try:
        choice = int(choice_str)
    except:
        choice = 0
    if choice < 1 or choice >= len(characters):
        await message.channel.send(f"Invalid character# (choose from 1 through {len(characters) - 1})")
        return
    player_to_preferred_character[message.author] = characters[choice]
    await message.channel.send(f"Your preferred character is now **{player_to_preferred_character[message.author].name}**.")

# If both players have compatible preferences, award them both
# If only one player has a preference, award it and choose a random for the other
# If both players have the same preference, choose one randomly, award it, then choose a random for the other
# If neither player has a preference, choose a random for each one
def choose_characters(player1: discord.Member, player2: discord.Member):
    char1 = chararacter_or_none(player1)
    char2 = chararacter_or_none(player2)
    if (char1 == char2) and (char1 is not None):
        (char1, char2) = contested_selection(player1, player2)
    if char1 is None:
        char1 = random_character_except(char2)
    if char2 is None:
        char2 = random_character_except(char1)
    return (random_material_for_character(char1), random_material_for_character(char2))

def chararacter_or_none(player: discord.Member):
    if player in player_to_preferred_character:
        return player_to_preferred_character[player]
    return None

#returns a random character except the one passed in
def random_character_except(character):
    random_char = random.choice(characters[1:])
    while random_char == character:
        random_char = random.choice(characters[1:])
    return random_char

def contested_selection(player1: discord.Member, player2: discord.Member):
    winner = random.choice((player1, player2))
    if winner == player1:
        return (player_to_preferred_character[player1], random_character_except(player_to_preferred_character[player1]))
    else:
        return (player_to_preferred_character[player2], random_character_except(player_to_preferred_character[player2]))

def random_material_for_character(character):
    return random.choice(character.filenames)
