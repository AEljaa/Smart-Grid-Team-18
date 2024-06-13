import requests
import json
import pandas as pd
import numpy as np
import joblib
url="http://127.0.0.1:4000/helper" #from our flask api
#model = joblib.load("ml.pkl")
model = joblib.load(r"C:\Users\Student\Desktop\summerproj\SummerProjWeb\multithreadserver\ml.pkl")
wallet=0

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

def algorithm(MaxAmount):    
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
        res=MaxAmount*ratio*-1
    if incr:
        res=MaxAmount*ratio
    return res


def return_irradiance():
    _,_,_,_,_,irradiance = fetch_latest()
    return irradiance


def return_demand():
    _,_,_,_,demand,_=fetch_latest()
    leftforfefferable=4-demand


    return demand


def deferablehell(Tick, freepower,derablelist,demand ):
    ratiolist=[]
    for deferable in derablelist:
        if deferable[2]<= Tick:
            ratiolist.append(deferable[1] / (deferable[0]-deferable[2]))
    max=0
    postion=0
    for i in range (0, len(ratiolist)):
        if ratiolist[i]>= max:
            postion=i
    
    
    if derablelist[postion][1]-5*freepower >=0: 
        derablelist[postion][1]=derablelist[postion][1]-5*freepower
        return 4
    else:
        derablelist[postion][1]=derablelist[postion][1]-5*freepower
        return (derablelist[postion][1]/5)+demand
        
 
