import json

def make_output(description: str, url: str):
    output = {}
    output["description"] = description
    output["url"] = url
    return output

liz_stone = {}
liz_stone["name"] = "Liz Harper"

stage1 = []
stage1.append(make_output("You are ready for action! You eagerly brandish your flask of transformative elixir.", "https://cdn.discordapp.com/attachments/514279423688835087/736409976138104852/Liz_Level1_Pose1_Camera_1.png"))
stage1.append(make_output("Your new experimental flask is ready to go. Your opponent won't know what hit her.", "https://cdn.discordapp.com/attachments/514279423688835087/736410006143893505/Liz_Level1_Pose2_Camera_1.png"))

stage2 = []
stage2.append(make_output("The attack destroys your clothes, leaving you in just a tank and ripped shorts. Bothersome, but nothing you can't handle.", "https://media.discordapp.net/attachments/514279423688835087/736410508286099526/Liz_Level2_Pose1_Camera_1.png"))
stage2.append(make_output("The attack leaves you in little more than your underwear. At least you can move around easily for now.", "https://media.discordapp.net/attachments/514279423688835087/736410524757000202/Liz_Level2_Pose2_Camera_1.png"))

liz_stone["stages"] = [] 
liz_stone["stages"].append(stage1)
liz_stone["stages"].append(stage2)

with open('liz_stone.json', 'w') as fp:
    json.dump(liz_stone, fp)