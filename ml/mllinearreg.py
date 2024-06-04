import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.arrays.base import mode
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
import joblib
import requests
url="http://127.0.0.1:4000/helper" #from our flask api
wallet=0
def fetch_latest():
    source = requests.get(url).json()
    lags=source["lags"]
    price=source['current_sell_price']
    demand=source['demand']
    inputData=pd.DataFrame(
        {
            "demandHist": demand,
            "Lag_1": lags[-1],
            "Lag_2": lags[-2],
            "Lag_3": lags[-3]

            },index=[0])
    return inputData,price

# Load historical data from CSV
df = pd.read_csv("historical_prices.csv")

#inputData=fetch_latest()

def futit(df, lag):
    names = []
    for i in range(1, lag + 1):
        names.append("fut_" + str(i))
        df["fut_" + str(i)] = df["sellHist"].shift(-i)
    return names


def lagit(df, lag):
    names = []
    for i in range(1, lag + 1):
        names.append("Lag_" + str(i))
        df["Lag_" + str(i)] = df["sellHist"].shift(i)
    return names

lagnames = lagit(df, 3)
futnames = futit(df,2)

df.dropna(inplace=True)

x = df[["demandHist"] + lagnames]
y = df[["sellHist"]+ futnames]

model = joblib.load("RandomForrestModelFut2.pkl")
while True:
    inputData,price=fetch_latest()
    predictedSellPrices=model.predict(inputData)
    grad = all(i < j for i, j in zip(predictedSellPrices[0], predictedSellPrices[0][1:]))#https://www.geeksforgeeks.org/python-check-if-list-is-strictly-increasing/  if pred array increases the nprice trending up, buy
    if grad:
        wallet -= price
        print("BUY: wallet",wallet)
    else:
        wallet+=price
        print("SELL: wallet",wallet)
    time.sleep(5)

