import pandas as pd
import os
import numpy as np
import joblib
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

path = "data/Formula 1 World Championship (1950 - 2023) Kaggle"

print("Loading data from csv files...")
df_races = pd.read_csv(path + "/races.csv")
df_results = pd.read_csv(path + "/results.csv")

# Minimum year for the data
min_year = 2022

# Filtering dataframes
df_races = df_races[df_races['year'] >= min_year]
df_results = df_results[df_results['raceId'].isin(df_races['raceId'])]


print("---- MODEL TRAINING ----")

# Sort the results to ensure chronological order
df_results_sorted = df_results.sort_values(by=['driverId', 'raceId'])

# Number of recent races to consider for the decay rate
X = 3  
# Decay rate to apply to each previous race
decay_rate = 0.9  

# Prepare the dataset
def prepare_dataset(df, X, decay_rate):
    weighted_positions = []

    # Iterate over each row in the dataframe
    for index, row in df.iterrows():
        driver_id = row['driverId']
        race_id = row['raceId']

        # Get the last X races for the driver before the current race
        previous_races = df[(df['driverId'] == driver_id) & (df['raceId'] < race_id)].tail(X)

        # Apply decay to each position
        weights = [decay_rate ** i for i in range(len(previous_races))]
        weighted_position = np.average(previous_races['positionOrder'], weights=weights) if not previous_races.empty else np.nan

        weighted_positions.append(weighted_position)

    df['weighted_position'] = weighted_positions
    return df

# Apply the function to prepare the dataset
df_prepared = prepare_dataset(df_results_sorted, X, decay_rate)

# Drop rows with NaN values
df_prepared = df_prepared.dropna()

# The feature is the weighted_position, and the label is the actual positionOrder of the next race
features = df_prepared[['weighted_position']]
labels = df_prepared['positionOrder']

# Train test split
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Create a new folder to save the model and the informations
# Get current date and time
now = datetime.now()

# Format as a string
folder_name = now.strftime("%Y-%m-%d_%Hh%M")

# Create the folder
os.makedirs(f"Models/{folder_name}", exist_ok=True)

# Evaluate the model and save the informations as a txt file
score = model.score(X_test, y_test)
with open(f"Models/{folder_name}/model_infos.txt", "w") as file:
    file.write(f"------ Model trained : {now.strftime('%Y-%m-%d %H:%M')} ------\n")
    file.write(f"- Decay rate: {decay_rate}\n")
    file.write(f"- X races: {X}\n")
    file.write(f"Model score: {score}\n")
    file.write("----------------------------------------------\n")

# Save the model
joblib.dump(model, f"Models/{folder_name}/model.pkl")

print("Model trained and saved successfully!")