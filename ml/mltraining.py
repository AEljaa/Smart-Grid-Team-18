import time
import joblib
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, precision_score, classification_report, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight

url="http://127.0.0.1:4000/helper" #from our flask api
wallet=0

def fetch_latest(new_preds):
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
    return inputData, price, tick, lags

# Load historical data from CSV
df = pd.read_csv("historical_prices.csv")

# Functions to create lag and future features
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
futnames = futit(df, 2)

horizons = [2, 5, 10, 15, 30, 60]
new_pred = []

for horizon in horizons:
    rolling_avg = df["sellHist"].rolling(horizon).mean()
    ratio_col = f"SellHist_ratio_{horizon}"
    df[ratio_col] = df["sellHist"] / rolling_avg
    trend_col = f"Trend_Sell{horizon}"
    df[trend_col] = df["sellHist"].shift(1).rolling(horizon).sum()
    new_pred += [ratio_col, trend_col]

df.dropna(inplace=True)

x = df[["demandHist", "tick"] + lagnames + new_pred]
y = df[["sellHist"] + futnames]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)


# Random Forest Regression
regressor = RandomForestRegressor(min_samples_split=100)

regressor.fit(x, y)
while regressor.score(x,y)<0.665:
    regressor.fit(x, y)
    print(regressor.score(x,y))
#    df.to_csv("df.csv")
# Save the trained regressor model
joblib.dump(regressor,"randforreg100minsplit3lag2futnewpreds066.pkl")
