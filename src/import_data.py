import pandas as pd
import os
import glob
import requests
import json
from datetime import datetime

def get_most_recent_dir():
    path_pattern = os.path.join("data/api_ergast", "*")
    directories = glob.glob(path_pattern)
    most_recent_dir = max(directories, key=os.path.getmtime)
    print("Checking latest data from: ",most_recent_dir)
    return most_recent_dir

def import_files(most_recent_dir):
    last_results = pd.read_csv(os.path.join(most_recent_dir + "/results.csv"))
    last_races = pd.read_csv(os.path.join(most_recent_dir + "/races.csv"))
    return last_results, last_races

def get_api_data():
    url = 'http://ergast.com/api/f1/current/last/results.json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data['MRData']['RaceTable']['Races']
        raceName = data['MRData']['RaceTable']['Races'][0]['raceName']
        return results, raceName
    else:
        return None, None

def check_new_data(results, raceName, last_results, last_races):
    for race in results:
        raceId = last_races[last_races['name'] == raceName].iloc[-1]['raceId']
        if raceId in last_results['raceId'].values:
            print("No new data.")
            return False
    print("New data available.")
    return True

def save_new_data(results, raceName, last_results, last_races):
    last_resultId = last_results.iloc[-1]['resultId']
    last_resultId += 1
    raceId = last_races[last_races['name'] == raceName].iloc[-1]['raceId']
    data = []

    for race in results:
        for result in race['Results']:
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

    df = pd.DataFrame(data)
    last_results = pd.concat([last_results, df], ignore_index=True)
    current_date = datetime.now().strftime('%Y-%m-%d_%Hh%M')
    new_dir = f'data/api_ergast/{current_date}'
    os.makedirs(new_dir, exist_ok=True)
    last_results.to_csv(f'{new_dir}/results.csv', index=False)
    print(f"\n--> Results saved in {new_dir} directory")
    last_races.to_csv(f'{new_dir}/races.csv', index=False)

def main():
    most_recent_dir = get_most_recent_dir()
    last_results, last_races = import_files(most_recent_dir)
    results, raceName = get_api_data()
    if check_new_data(results, raceName, last_results, last_races):
        save_new_data(results, raceName, last_results, last_races)

if __name__ == '__main__':
    main()