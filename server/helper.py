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
                print("File loaded, no API fetching")
        else: # tick is 0 our tick is 59
            deferablelist = source['deferables']
            ourtick = 59
            print("Tick is 0, data fetched from API")
    except OSError:
        deferablelist = source['deferables']
        ourtick = (tick -1) if tick !=0 else 59
        print("No file, data fetched from API")
    return demand, tick, deferablelist,ourtick

def cleanandsave(deferablelist,ourtick):
    invalid_keys = [key for key, deferable in deferablelist.items() if deferable[1] <= 0]
    for key in invalid_keys:
        print(f"Removing {deferablelist[key]} as value is <= 0")
        del deferablelist[key]
 #####
    deferablelist['ourtick'] = ourtick  # Add ourtick to the data
    with open(fname, 'w') as f:
        json.dump(deferablelist, f)

def fetch_latest():
    source = requests.get(url).json()
    lags = source["lags"]
    price = source['current_sell_price']
    demand = source['demand']
    tick = source['tick']
    irradiance = source["sun"]
    inputData = pd.DataFrame(
        {
            "demandHist": demand,
            "tick": tick,
            "Lag_1": lags[-1],
            "Lag_2": lags[-2],
            "Lag_3": lags[-3]
        }, index=[0])
    return inputData, price, tick, lags, demand, irradiance

def naive_algorithm(price, yesterday_list):
    if price < sum(yesterday_list) / len(yesterday_list):
        print("BUY")
    else:
        print("SELL")

def energyAlgorithm(currAmount):
    input, _, _, _, _, _ = fetch_latest()
    predicted_prices = model.predict(input)
    test_list = predicted_prices[0]
    decr = 0
    incr = 0
    ratio = return_demand() / 5
    res = 0
    decr = np.array_equal(test_list, sorted(test_list, reverse=True))
    incr = all(i < j for i, j in zip(predicted_prices[0], predicted_prices[0][1:]))  # if pred array increases, then price trending up, buy
    if decr:
        res = currAmount * ratio * -1  # sell
    if incr:
        res = (7 - currAmount) * (1 - ratio)  # buy
    return res + 0.25

def return_irradiance():
    _, _, _, _, _, irradiance = fetch_latest()
    return irradiance

def return_demand():
    _, _, _, _, demand, _ = fetch_latest()
    return demand

ourvalue = 4


def greedyDeferable():
    demand, tick, deferablelist, ourtick = loaddeferable()
    if not deferablelist:
        print("All deferables are processed, list is empty")
        return demand + 0.01 # No more, just do demand

    max_index = max(int(key) for key in deferablelist) if deferablelist else -1
    ratiolist = [0] * (max_index + 1)
    freepower = 4 - demand
    global ourvalue

    print("OURTICK", ourtick, "CURRENTTICK", tick)
    print("Demand:", demand, "Tick:", tick, "Deferable List:", deferablelist)

    if ourtick != tick:
        print("Current tick is not equal to our tick")
        for key, deferable in deferablelist.items():
            key_int = int(key)  # Convert key to integer
            print(f"Processing deferable {key}: {deferable}")
            if deferable[2] <= tick:
                ratiolist[key_int] = (deferable[1] / (deferable[0] - deferable[2]))
                print(f"Ratio for deferable {key}: {ratiolist[key_int]}")

        max_ratio = 0
        position = -1
        print("Ratio list",ratiolist)
        for i in range(len(ratiolist)):
            if ratiolist[i] >= max_ratio:
                position = i
                max_ratio = ratiolist[i]

        if position == -1:
            # No valid position found
            print("No valid deferable position found")

            ourtick = tick
            return (demand + 0.01)

        if (len(deferablelist) == 0):
            ourtick = tick
            return (demand + 0.01) # No deferable

        print(f"Selected deferable position: {position} with max ratio: {max_ratio}")
        deferable_key = str(position)  # Convert position back to string to access deferablelist
        if deferablelist[deferable_key][1] - (5 * freepower) >= 0:  # Maximize how much of the deferable we do
            deferablelist[deferable_key][1] -= 5 * freepower
            print("Deferable at", deferablelist[deferable_key], "has", deferablelist[deferable_key][1])
            ourtick = tick
            cleanandsave(deferablelist, ourtick)
            print("Assigning tick")
            ourvalue = 4
            return 4  # Tell load to max out since we are maximizing with greedy algo
        else:
            temp = deferablelist[deferable_key][1]
            deferablelist[deferable_key][1] = 0  # If less deferable energy than free room, use deferable amount + demand
            print("Deferable at", deferablelist[deferable_key], "has", deferablelist[deferable_key][1])
            ourtick = tick
            cleanandsave(deferablelist, ourtick)
            print("Assigning tick")
            ourvalue = temp/5 + demand
            return ourvalue # Convert deferable value back to power
    else:
        print("LED is on same tick")
        return ourvalue
