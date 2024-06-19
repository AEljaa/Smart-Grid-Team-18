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
                deferablelist = json.load(f)
                print("File loaded, no API fetching")
        else:
            deferablelist = source['deferables']
            print("Tick is 0, data fetched from API")
    except OSError:
        deferablelist = source['deferables']
        print("No file, data fetched from API")
    return demand, tick, deferablelist

def cleanandsave(data):
    invalid_keys = [key for key, deferable in data.items() if deferable[1] <= 0]
    for key in invalid_keys:
        print(f"Removing {data[key]} as value is <= 0")
        del data[key]
    with open(fname, 'w') as f:
        json.dump(data, f)

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
        res = (45 - currAmount) * (1 - ratio)  # buy
    return res

def return_irradiance():
    _, _, _, _, _, irradiance = fetch_latest()
    return irradiance

def return_demand():
    _, _, _, _, demand, _ = fetch_latest()
    return demand

ourtick = 0
ourvalue = 4

def greedyDeferable():
    demand, tick, deferablelist = loaddeferable()
    ratiolist = [0] * 3
    freepower = 4 - demand
    global ourtick
    global ourvalue
    print("OURTICK", ourtick, "CURRENTTICK", tick)
    print("Demand:", demand, "Tick:", tick, "Deferable List:", deferablelist)
    
    if not deferablelist:
        print("All deferables are processed, list is empty")
        return demand  # no more, just do demand
    
    if ourtick != tick:
        print("Current tick is not equal to our tick")
        for key, deferable in deferablelist.items():
            if deferable[2] <= tick:
                ratiolist[int(key)] = (deferable[1] / (deferable[0] - deferable[2]))
        max_ratio = 0
        position = 0
        
        for i in range(len(ratiolist)):
            if ratiolist[i] >= max_ratio:
                position = i
                max_ratio = ratiolist[i]
        
        if deferablelist[str(position)][1] - 5 * freepower >= 0:  # Maximize how much of the deferable we do
            deferablelist[str(position)][1] -= 5 * freepower
            print("Deferable at", deferablelist[str(position)], "has", deferablelist[str(position)][1])
            cleanandsave(deferablelist)
            ourtick = tick
            ourvalue = 4
            return 4  # tell load to max out since we are maximizing with greedy algo
        else:
            deferablelist[str(position)][1] -= 5 * freepower  # if less deferable energy than free room, use deferable amount + demand
            print("Deferable at", deferablelist[str(position)], "has", deferablelist[str(position)][1])
            cleanandsave(deferablelist)
            ourtick = tick
            ourvalue = (deferablelist[position][1] / 5) + demand
            return (deferablelist[position][1] / 5) + demand  # convert deferable value back to power
    else:
        print("LED is on same tick")
        return ourvalue
