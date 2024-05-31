from operator import index
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error, r2_score
import joblib
import requests
url="http://127.0.0.1:4000/helper" #from our flask api

def fetch_latest():
    source = requests.get(url).json()
    lags=source["lags"]
    price=source['current_sell_price']
    demand=source['demand']
    return lags,price,demand

# Load historical data from CSV
df = pd.read_csv("historical_prices.csv")

def lagit(df, lag):
    names = []
    for i in range(1, lag + 1):
        names.append("Lag_" + str(i))
        df["Lag_" + str(i)] = df["sellHist"].shift(i)
    return names

lagnames = lagit(df, 3)
df.dropna(inplace=True)

x = df[["demandHist"] + lagnames]
y = df["sellHist"]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

model = joblib.load('lasso_model.pkl')
lags,price,demand=fetch_latest()
#joblib.dump(model, 'lasso_model.pkl')
inputdata=pd.DataFrame(
        {
            'demandHist':demand,
            'Lag_1' : lags[-1],
            'Lag_2': lags[-2],
            'Lag_3': lags[-3]
            },index=[0])

model.fit(x_train, y_train)
predicted_sell_price = model.predict(inputdata)[0]

if predicted_sell_price > price:
    decision = "buy"
else:
    decision = "sell"

print(decision)
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

y_pred = model.predict(x_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
absol_err= mean_absolute_error(y_test,y_pred)
print("Mean Absolutw Error:", absol_err)
print("Mean Squared Error:", mse)
print("R² Score:", r2)


