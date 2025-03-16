from random import randint
import time


def smarthome():
    max_power = 4000
    kettle_power = 2000
    dishwasher_power = 1700
    oven_power = 3000
    boiler_power = 1500
    stove_power = 1000

    mod = input("enter the mod of kettle(on/off): ")
    kettle = kettle_power if (mod == "on") else 0
    mod = input("enter the mod of dishwasher(on/off): ")
    dishwasher = dishwasher_power if (mod == "on") else 0
    mod = input("enter the mod oven(on/off): ")
    oven = oven_power if (mod == "on") else 0
    mod = input("enter the mod boiler(on/off): ")
    boiler = boiler_power if (mod == "on") else 0
    mod = input("enter the mod of stove(on/off): ")
    stove = stove_power if (mod == "on") else 0

    total_power = kettle + dishwasher + oven + boiler + stove

    if boiler and total_power >= 3000:
        boiler = 0
        print("Boiler turned off (>= 3000W)")

    if kettle and dishwasher and oven and total_power < 2500:
        boiler = boiler_power
        print("Boiler turned on (< 2500W)")

    if dishwasher and not boiler and total_power >= 3900:
        dishwasher = 0
        print("Dishwasher turned off (>= 3900W)")

    if not dishwasher and oven and kettle and total_power < 1900:
        dishwasher = dishwasher_power
        print("Dishwasher turned on (< 1900W)")

    if oven and boiler and total_power >= 3900:
        oven = 0
        print("Oven turned off (>= 3900W)")

    if not oven and kettle and total_power < 1900:
        oven = oven_power
        print("Oven turned on (< 1900W)")

    if kettle and boiler and total_power >= 3900:
        kettle = 0
        print("Kettle turned off (>= 3900W)")

    if not kettle and total_power < 1900:
        kettle = kettle_power
        print("Kettle turned on (< 1900W)")

    print(f"Current power consumption: {kettle + dishwasher + oven + boiler + stove}W")


while True:
    smarthome()