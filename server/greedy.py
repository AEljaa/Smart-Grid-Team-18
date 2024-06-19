import requests
import json
import pandas as pd
import numpy as np
import joblib

url = "http://127.0.0.1:4000/helper"  # from our flask api
model = joblib.load("ml.pkl")
#model = joblib.load(r"C:\Users\Student\Desktop\summerproj\SummerProjWeb\multithreadserver\ml.pkl")
fname = "../db/deferable_db.json"  # our json database, if it doesn't exist, it gets made

def loaddeferable():
    source = requests.get(url).json()
    demand = source['demand']
    tick = source['tick']
    try:
        if tick != 0:

            with open(fname, 'r+b') as f:
                data = json.load(f)
                filtered_data = {key: value for key, value in data.items() if key.isdigit()}
                print(filtered_data)
                ourtick = data.get('ourtick', 0)  # Get ourtick from the file, default to 0 if not found
                deferablelist =filtered_data
        else: # tick is 0 our tick is 59
            deferablelist = source['deferables']
            ourtick = 59
    except OSError:
        deferablelist = source['deferables']
        ourtick = (tick -1) if tick !=0 else 59
    return demand, tick, deferablelist,ourtick

def cleanandsave(deferablelist,ourtick):
    invalid_keys = [key for key, deferable in deferablelist.items() if deferable[1] <= 0]
    for key in invalid_keys:
        del deferablelist[key]
 #####
    deferablelist['ourtick'] = ourtick  # Add ourtick to the data
    with open(fname, 'w') as f:
        json.dump(deferablelist, f)

def greedyDeferable():
    demand, tick, deferablelist, ourtick = loaddeferable()
    if not deferablelist:
        return demand + 0.01 # No more, just do demand

    max_index = max(int(key) for key in deferablelist) if deferablelist else -1
    ratiolist = [0] * (max_index + 1) ##only have ratios for how many deferabels there are
    freepower = 4 - demand
    global ourvalue

    print("OURTICK", ourtick, "CURRENTTICK", tick)

    if ourtick != tick:
        for key, deferable in deferablelist.items():
            key_int = int(key)  # Convert key to integer
            if deferable[2] <= tick:
                print("Current tick",tick ," Deferable",deferable)
                ratiolist[key_int] = (deferable[1] / (deferable[0] - deferable[2]))

        print("Current Ratio list",ratiolist)
        max_ratio = 0
        position = -1
        for i in range(len(ratiolist)):
            if ratiolist[i] >= max_ratio:
                position = i
                max_ratio = ratiolist[i]

        if position == -1:
            # No valid position found

            ourtick = tick
            return (demand + 0.01)

        if (len(deferablelist) == 0):
            ourtick = tick
            return (demand + 0.01) # No deferable

        deferable_key = str(position)  # Convert position back to string to access deferablelist
        if deferablelist[deferable_key][1] - 5 * freepower >= 0:  # Maximize how much of the deferable we do
            deferablelist[deferable_key][1] -= 5 * freepower
            ourtick = tick
            cleanandsave(deferablelist, ourtick)
            ourvalue = 4
            return 4  # Tell load to max out since we are maximizing with greedy algo
        else:
            deferablelist[deferable_key][1] -= 5 * freepower  # If less deferable energy than free room, use deferable amount + demand
            ourtick = tick
            cleanandsave(deferablelist, ourtick)
            ourvalue = (deferablelist[deferable_key][1] / 5) + demand
            return (deferablelist[deferable_key][1] / 5) + demand  # Convert deferable value back to power
    else:
        print("LED is on same tick")
        return demand


while True:
    greedyDeferable()
