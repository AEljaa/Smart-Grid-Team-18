import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load historical data from CSV
df = pd.read_csv("historical_prices.csv")

# Add a time tick column
df["tick"] = np.arange(len(df.index))

# Feature and target for time-series model
X_ts = df[["tick"]]
Y_ts = df["sellHist"]

# Train the linear regression model
model_ts = LinearRegression()
model_ts.fit(X_ts, Y_ts)

# Predict values
y_pred_ts = pd.Series(model_ts.predict(X_ts))

# Evaluate the time-series model
mse_ts = mean_squared_error(Y_ts, y_pred_ts)
r2_ts = r2_score(Y_ts, y_pred_ts)
print(f"Time-series model - MSE: {mse_ts}, R²: {r2_ts}")

# Add lag feature
df["Lag_1"] = df["sellHist"].shift(1)
df_lag = df.dropna()

# Feature and target for lag model
X_lag = df_lag[["Lag_1"]]
Y_lag = df_lag["sellHist"]

# Train the linear regression model with lag feature
model_lag = LinearRegression()
model_lag.fit(X_lag, Y_lag)

# Predict values
y_pred_lag = pd.Series(model_lag.predict(X_lag))

# Evaluate the lag model
mse_lag = mean_squared_error(Y_lag, y_pred_lag)
r2_lag = r2_score(Y_lag, y_pred_lag)
print(f"Lag feature model - MSE: {mse_lag}, R²: {r2_lag}")

# Plotting
plt.figure(figsize=(11, 4))
plt.plot(X_ts, Y_ts, label="Actual", color='blue')
plt.plot(X_ts, y_pred_ts, label="Predicted (Time-series)", linestyle='--', color='orange')
plt.scatter(X_lag, Y_lag, label="Actual (Lag)", color='blue', alpha=0.5)
plt.plot(X_lag, y_pred_lag, label="Predicted (Lag)", linestyle='--', color='green')
plt.xlabel("Ticks")
plt.ylabel("Sell Price")
plt.title("Linear Regression Models Comparison")
plt.legend()
plt.show()

