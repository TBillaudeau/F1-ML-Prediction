import pandas as pd
import os
import glob
import requests
import json
from datetime import datetime

# We read the most recent results.csv and races.csv files
path_pattern = os.path.join("data/api_ergast", "*")
directories = glob.glob(path_pattern)
most_recent_dir = max(directories, key=os.path.getmtime)
print("Checking latest data from: ",most_recent_dir)

# Importing the files
last_results = pd.read_csv(os.path.join(most_recent_dir + "/results.csv"))
last_races = pd.read_csv(os.path.join(most_recent_dir + "/races.csv"))

# We import the latest results from the api
url = 'http://ergast.com/api/f1/current/last/results.json'
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    results = data['MRData']['RaceTable']['Races']
    raceName = data['MRData']['RaceTable']['Races'][0]['raceName']

# Loop through the API results
for race in results:
    raceId = last_races[last_races['name'] == raceName].iloc[-1]['raceId']

    # We check if this raceId already exists in the last_results DataFrame
    if raceId in last_results['raceId'].values:
        print("No new data.")
        break
    else:
        print("New data available.")
        # We then save the new data !

        # Lets start by getting the last resultId from the existing csv
        last_resultId = last_results.iloc[-1]['resultId']
        last_resultId += 1

        # We then need to get the raceId by matching raceName to the list of races from the last_races csv and get the most recent one
        raceId = last_races[last_races['name'] == raceName].iloc[-1]['raceId']

        data = []

        for race in results:
            for result in race['Results']:
                driverId = result['Driver'].get('driverId', None)
                constructorId = result['Constructor'].get('constructorId', None)
                driverNumber = result.get('number', None)
                gridPosition = result.get('grid', None)
                positionOrder = result.get('position', None)
                points = result.get('points', None)
                laps = result.get('laps', None)
                time = result['Time'].get("time", None) if 'Time' in result else None
                milliseconds = result['Time'].get("millis", None) if 'Time' in result else None
                fastestLap = result['FastestLap'].get("lap", None) if 'FastestLap' in result else None
                rankFastestLap = result['FastestLap'].get("rank", None) if 'FastestLap' in result else None
                fastestLapTime = result['FastestLap']['Time'].get("time", None) if 'FastestLap' in result and 'Time' in result['FastestLap'] else None
                fastestLapSpeed = result['FastestLap']['AverageSpeed'].get("speed", None) if 'FastestLap' in result and 'AverageSpeed' in result['FastestLap'] else None
                status = result.get('status', None)

                data.append({
                    'resultId': last_resultId,
                    'raceId': raceId,
                    'driverId': driverId,
                    'constructorId': constructorId,
                    'number': driverNumber,
                    'grid': gridPosition,
                    'position': positionOrder,
                    'positionText': positionOrder,
                    'positionOrder': positionOrder,
                    'points': points,
                    'laps': laps,
                    'time': time,
                    'milliseconds': milliseconds,
                    'fastestLap': fastestLap,
                    'rank': rankFastestLap,
                    'fastestLapTime': fastestLapTime,
                    'fastestLapSpeed': fastestLapSpeed,
                    'statusId': status
                })

                last_resultId += 1

        # Convert the list of dictionaries into a DataFrame
        df = pd.DataFrame(data)

        # Now add all data from df to last_results
        last_results = pd.concat([last_results, df], ignore_index=True)

        # Save to directory
        
        # Get current date and time
        current_date = datetime.now().strftime('%Y-%m-%d_%Hh%M')

        # Create new directory
        new_dir = f'data/api_ergast/{current_date}'
        os.makedirs(new_dir, exist_ok=True)

        # Save the file in the new directory
        last_results.to_csv(f'{new_dir}/results.csv', index=False)

        print(f"\n--> Results saved in {new_dir} directory")

        # Also add the races.csv file
        last_races.to_csv(f'{new_dir}/races.csv', index=False)