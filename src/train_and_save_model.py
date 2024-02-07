import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib
import os
import glob
import datetime
import pickle

def get_most_recent_dir():
    path_pattern = os.path.join("data/api_ergast", "*")
    directories = glob.glob(path_pattern)
    most_recent_dir = max(directories, key=os.path.getmtime)
    print("Checking latest data from: ",most_recent_dir)
    return most_recent_dir

def load_datasets(folder_path):
    races_df = pd.read_csv(f'{folder_path}/races.csv')
    results_df = pd.read_csv(f'{folder_path}/results.csv')
    return races_df, results_df

def preprocess_and_select_features(races_df, results_df):
    df = pd.merge(races_df[['raceId','circuitId']], results_df[['raceId', 'driverId', 'constructorId', 'grid', 'positionOrder']], on='raceId')
    df = df.dropna()
    X = df[['grid', 'constructorId', 'driverId','circuitId']]
    y = df['positionOrder']
    return X, y

def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    print(f"RMSE: {rmse}")
    print(f"Accuracy: {model.score(X_test, y_test)}")

def save_model(model, filenameJobLib, filenamePickle):
    joblib.dump(model, filenameJobLib)
    with open(filenamePickle, 'wb') as file:  # Use 'wb' to write in binary mode
        pickle.dump(model, file)

def write_performance_to_file(model, X_test, y_test, X_train, filename):
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    accuracy = model.score(X_test, y_test)
    data_quantity = len(X_train) + len(X_test)

    with open(filename, 'w') as f:
        f.write(f"RMSE: {rmse}\n")
        f.write(f"Accuracy: {accuracy}\n")
        f.write(f"Quantity of data: {data_quantity}\n")

def main():
    most_recent_dir = get_most_recent_dir()
    races_df, results_df = load_datasets(most_recent_dir)
    X, y = preprocess_and_select_features(races_df, results_df)
    X_train, X_test, y_train, y_test = split_data(X, y)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

    # Save model to new folder in Models
    current_date = datetime.datetime.now().strftime('%Y-%m-%d_%Hh%M')
    new_dir = f'Models/{current_date}'
    os.makedirs(new_dir, exist_ok=True)
    save_model(model, f'{new_dir}/random_forest_regressor_model.joblib', f'{new_dir}/random_forest_regressor_model.pkl')

    # Write performance metrics to a text file
    write_performance_to_file(model, X_test, y_test, X_train, f'{new_dir}/model_performance.txt')

if __name__ == '__main__':
    main()