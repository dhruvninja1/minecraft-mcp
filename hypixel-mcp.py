import skyblockpy
import pprint
import os

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
    

