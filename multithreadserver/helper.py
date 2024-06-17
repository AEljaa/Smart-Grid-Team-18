import requests
import json
import pandas as pd
import numpy as np
import joblib
url="http://127.0.0.1:4000/helper" #from our flask api
#model = joblib.load("ml.pkl")
model = joblib.load(r"C:\Users\Student\Desktop\summerproj\SummerProjWeb\multithreadserver\ml.pkl")

fname="deferable_db.json" #our json database, if it doesnt exist, it gets made
def loaddeferable():
    source = requests.get(url).json()
    demand = source['demand']
    tick = source['tick']
    try:
        if tick != 0:
            with open(fname, 'r+b') as f:
                deferablelist=json.load(f)
                print("file loaded no api fetching")
        else:
            deferablelist = source ['deferables']
            print("tick is 0, data fetched from api")
    except OSError:
        deferablelist = source ['deferables']
        print("no file, data fetched from api")
    return demand,tick,deferablelist

def cleanandsave(data):
    invalid_keys = [key for key, deferable in data.items() if deferable[1] <= 0]
   
    for key in invalid_keys:
        print(f"Removing {data[key]} as value is <=0")
        del data[key]    

    with open('jsondb.json', 'w') as f:
        json.dump(data, f)

def fetch_latest():
    source = requests.get(url).json()
    lags = source["lags"]
    price = source['current_sell_price']
    demand = source['demand']
    tick = source['tick']
    irradiance = source ["sun"]
    inputData = pd.DataFrame(
        {
            "demandHist": demand,
            "tick": tick,
            "Lag_1": lags[-1],
            "Lag_2": lags[-2],
            "Lag_3": lags[-3]
        }, index=[0])
    return inputData, price, tick, lags,demand,irradiance


def naive_algorithm(price,yesterday_list):
    if(price < sum(yesterday_list)/len(yesterday_list)):
        print("BUY")
    else:
        print("SELL")

def energyAlgorithm(MaxAmount):    
    input,_,_,_,_,_=fetch_latest()
    predicted_prices=model.predict(input)
    test_list=predicted_prices[0]
    decr=0
    incr=0
    ratio=return_demand()/5
    res=0
    decr = np.array_equal(test_list, sorted(test_list, reverse=True))
    incr = all(i < j for i, j in zip(predicted_prices[0], predicted_prices[0][1:]))#https://www.geeksforgeeks.org/python-check-if-list-is-strictly-increasing/  if pred array increases the nprice trending up, buy
    if(decr):
        res=(46-MaxAmount)*ratio*-1
    if incr:
        res=MaxAmount*(1-ratio)
    return res


def return_irradiance():
    _,_,_,_,_,irradiance = fetch_latest()
    return irradiance


def return_demand():
    _,_,_,_,demand,_=fetch_latest()
    return demand


def greedyDeferable(freepower):
    demand,tick,deferablelist=loaddeferable()
    ratiolist=[0]*3
    data=deferablelist
    # Check if deferablelist is empty and return early
    if not deferablelist:
        print("All deferables are processed list is empty")
        return demand # no more, just do demand
    for key,deferable in data.items():
        if deferable[2] <= tick:
           ratiolist[int(key)]=(deferable[1] / (deferable[0]-deferable[2]))
    max=0
    postion=0
    #if deferable now at 0, remove
    for i in range (0, len(ratiolist)):
        if ratiolist[i]>= max:
            postion=i
            max=ratiolist[i]
    
    
    if deferablelist[str(postion)][1]-5*freepower >=0: #We maximise how much of the deferable we do - take this away from the amount we are storing 
        deferablelist[str(postion)][1]=deferablelist[str(postion)][1]-5*freepower
        print("Deferable at",deferablelist[str(postion)], "has ", deferablelist[str(postion)][1] )
        cleanandsave(data)
        return 4 #tell load to max out since we are maximising with greedy algo
    else:
        deferablelist[str(postion)][1]=deferablelist[str(postion)][1]-5*freepower #if there is less deferable energy than the free room, then dont use all free room, just do deferable amount + demand
        print("Deferable at",deferablelist[str(postion)], "has ", deferablelist[str(postion)][1] )
        cleanandsave(data)
        return (deferablelist[postion][1]/5)+demand #deferable value is in Joules so we need to convert it back to power by dividing by 5
        
