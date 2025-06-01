import skyblockpy
import pprint
import os
import base64
import zlib
from fastmcp import FastMCP


mcp = FastMCP("My minecraft mcp server")



API_KEY_VAR_NAME = "HYPIXEL_API_KEY"
hypixel_api_key = os.getenv(API_KEY_VAR_NAME)




skyblock = skyblockpy.Skyblock(hypixel_api_key)

bzdata = skyblock.get_bazaar_data()["products"]







@mcp.tool()
def find_margins(product_name : str ="all", top: int = -1, instahourly: float = 0, purse_requirement = "no") -> list or int: #type: ignore
    if purse_requirement != "no":
        purse = get_purse("dhruvninja")
    else:
        purse = 500000000000000000
    if product_name == "all":
        margins = []
        for key in bzdata:
            if (float(bzdata[key]["quick_status"]["buyMovingWeek"]) >= instahourly * 24 * 7 and float(bzdata[key]["quick_status"]["sellMovingWeek"]) >= instahourly * 24 * 7 ) and purse >= float(bzdata[key]["quick_status"]["sellPrice"]):
                margins.append((key, int(float(bzdata[key]["quick_status"]["buyPrice"]) - float(bzdata[key]["quick_status"]["sellPrice"])))) 
        if top == -1:
            return margins    
        else:
            n = len(margins)
            swapped=False
            for i in range(n-1):
                swapped = False
                for j in range(n-1-i):
                    if margins[j][1] > margins[j+1][1]:
                        margins[j], margins[j+1] = margins[j+1], margins[j]
                        swapped=True
                if not swapped:
                    break
            margins.reverse()
            return margins[0:top]


    else:
        return int(float(bzdata[product_name]["quick_status"]["buyPrice"]) - float(bzdata[product_name]["quick_status"]["sellPrice"]))

@mcp.tool()
def get_purse(username : str, profile : str="selected") -> dict or int: #type: ignore
    playerdata = skyblock.get_player_profile(username)
    uuid = skyblock.get_uuid(username)
    profile = profile.capitalize()
    
    if profile != "Selected":
        coins = {}
        for x in range(len(playerdata["profiles"])):
            try:
                coins[playerdata["profiles"][x]["cute_name"]] = playerdata["profiles"][x]["members"][uuid]["currencies"]["coin_purse"]
            except KeyError:
                coins[playerdata["profiles"][x]["cute_name"]] = None
        return int(coins[profile])

    else:
        for x in range(len(playerdata["profiles"])):
            if playerdata["profiles"][x]["selected"]:
                selected = x
                break
        return int(playerdata["profiles"][selected]["members"][uuid]["currencies"]["coin_purse"])

@mcp.tool()
def data_decode(data : str) -> str: 
    decoded_data = base64.b64decode(data)

    try:
        decompressed_data = zlib.decompress(decoded_data, 16 + zlib.MAX_WBITS)
    except zlib.error as e:
        decompressed_data = zlib.decompress(decoded_data)
    readable_data = decompressed_data.decode('utf-8', errors='ignore')
    return readable_data





if __name__ == "__main__":
      mcp.run()