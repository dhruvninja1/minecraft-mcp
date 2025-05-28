import skyblockpy
import pprint
import os
import base64
import zlib

API_KEY_VAR_NAME = "HYPIXEL_API_KEY"
hypixel_api_key = os.getenv(API_KEY_VAR_NAME)

if hypixel_api_key:
    print(f"Successfully loaded API Key from environment variable")
else:
    print(f"Error: Environment variable '{API_KEY_VAR_NAME}' not found.")
    print("Please set it before running this script.")
    print("Example (Linux/macOS): export HYPIXEL_API_KEY=\"your_key_here\"")
    print("Example (Windows CMD): set HYPIXEL_API_KEY=\"your_key_here\"")
    exit()


skyblock = skyblockpy.Skyblock(hypixel_api_key)

bzdata = skyblock.get_bazaar_data()["products"]








def find_margins(product_name="all"):
    if product_name == "all":
        margins = []
        for key in bzdata:
            margins.append((key, float(bzdata[key]["quick_status"]["sellPrice"]) - float(bzdata[key]["quick_status"]["buyPrice"])))
        return margins
    else:
        return(float(bzdata[product_name]["quick_status"]["sellPrice"]) - float(bzdata[product_name]["quick_status"]["buyPrice"]))
    




def get_purse(username, profile="all"):
    playerdata = skyblock.get_player_profile(username)
    uuid = skyblock.get_uuid(username)
    profile = profile.capitalize()
    coins = {}

    for x in range(len(playerdata["profiles"])):
        try:
            coins[playerdata["profiles"][x]["cute_name"]] = playerdata["profiles"][x]["members"][uuid]["currencies"]["coin_purse"]
        except KeyError:
            coins[playerdata["profiles"][x]["cute_name"]] = None
    if profile != "All":
        return coins[profile]
    else:
        return coins

def data_decode(data):
    decoded_data = base64.b64decode(data)

    try:
        decompressed_data = zlib.decompress(decoded_data, 16 + zlib.MAX_WBITS)
    except zlib.error as e:
        decompressed_data = zlib.decompress(decoded_data)
    readable_data = decompressed_data.decode('utf-8', errors='ignore')
    return readable_data



