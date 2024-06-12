import requests
import json
import pandas as pd
import numpy as np
import joblib
url="http://127.0.0.1:4000/helper" #from our flask api
model=joblib.load("ml.pkl")#load ml model
wallet=0
def fetch_latest():
    source = requests.get(url).json()
    lags = source["lags"]
    price = source['current_sell_price']
    demand = source['demand']
    tick = source['tick']
    inputData = pd.DataFrame(
        {
            "demandHist": demand,
            "tick": tick,
            "Lag_1": lags[-1],
            "Lag_2": lags[-2],
            "Lag_3": lags[-3]
        }, index=[0])
    return inputData, price, tick, lags,demand


def naive_algorithm(price,yesterday_list):
    if(price < sum(yesterday_list)/len(yesterday_list)):
        print("BUY")
    else:
        print("SELL")

def algorithm(): #Sophie's aproach - need to refine within quartiles 2 and 3 (currently do nothing)
    input,_,_,_,_=fetch_latest()
    predicted_prices=model.predict(input)
    test_list=predicted_prices[0]
    print(test_list)
    decr=0
    incr=0
    ratio=1+return_demand()/4
    res=""
    decr = np.array_equal(test_list, sorted(test_list, reverse=True))
    incr = all(i < j for i, j in zip(predicted_prices[0], predicted_prices[0][1:]))#https://www.geeksforgeeks.org/python-check-if-list-is-strictly-increasing/  if pred array increases the nprice trending up, buy
    if(decr):
        res="SELL"
    if incr:
        res="BUY"
    value= {
        "instruction" : res,
        "ratio" : ratio
    }
    return value




def return_demand():
    _,_,_,_,demand=fetch_latest()
    return demand


    
if __name__ == "__main__":
    algorithm()



