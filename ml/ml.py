
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE

# Load historical data from CSV
csv_path = 'historical_prices.csv'
data = pd.read_csv(csv_path)

# Feature engineering
data['price_diff'] = data['sellHist'] - data['buyHist']
data['avg_buy'] = data['buyHist'].rolling(window=5).mean()
data['avg_sell'] = data['sellHist'].rolling(window=5).mean()
data['avg_demand'] = data['demandHist'].rolling(window=5).mean()
data = data.dropna()

# Labeling: Example strategy to label data
data['label'] = (data['sellHist'].shift(-1) > data['sellHist'] * 1.01).astype(int)
data = data.dropna()

# Prepare features and labels
features = ['buyHist', 'sellHist', 'price_diff', 'avg_buy', 'avg_sell', 'demandHist', 'avg_demand']
X = data[features]
y = data['label']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Handle class imbalance using SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# Hyperparameter tuning for RandomForest
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
}

grid_search = GridSearchCV(estimator=RandomForestClassifier(random_state=42), param_grid=param_grid,
                           cv=5, n_jobs=-1, verbose=2)

grid_search.fit(X_resampled, y_resampled)
best_model = grid_search.best_estimator_

# Evaluate the best model
y_pred = best_model.predict(X_test)
print(classification_report(y_test, y_pred))

# Fetch real-time data and make predictions
def fetch_real_time_data():
    # Implement your API call here to fetch current buy and sell prices
    # For demonstration, we'll use dummy values
    return {'buyHist': 115, 'sellHist': 57, 'demandHist': 2.793}

real_time_data = fetch_real_time_data()

# Mapping real-time data to the same feature names used in training
real_time_features = pd.DataFrame([{
    'buyHist': real_time_data['buyHist'],
    'sellHist': real_time_data['sellHist'],
    'price_diff': real_time_data['sellHist'] - real_time_data['buyHist'],
    'avg_buy': data['avg_buy'].iloc[-1],  # Using the last known rolling average from historical data
    'avg_sell': data['avg_sell'].iloc[-1],  # Using the last known rolling average from historical data
    'demandHist': real_time_data['demandHist'],
    'avg_demand': data['avg_demand'].iloc[-1]  # Using the last known rolling average from historical data
}], columns=features)  # Ensure the columns are in the correct order

# Make prediction
prediction = best_model.predict(real_time_features)
action = 'sell' if prediction[0] == 1 else 'hold'
print(f"Recommended action: {action}")
