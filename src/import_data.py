import requests
import pandas as pd
import os
from datetime import datetime

def get_drivers_standings(year='current'):
    url = f'http://ergast.com/api/f1/{year}/driverStandings.json'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        
        standings_list = []
        for position, driver_info in enumerate(standings, start=1):
            driver = driver_info['Driver']
            name = f"{driver['givenName']} {driver['familyName']}"
            points = driver_info['points']
            standings_list.append([position, name, points])
        
        df = pd.DataFrame(standings_list, columns=['Position', 'Name', 'Points'])

        print("\n--> Showing first rows of data ---------")
        print(df.head(4))
        print("---------------------------------------\n")

        # Get current date and time
        current_date = datetime.now().strftime('%Y-%m-%d_%Hh%M')

        # Create new directory
        new_dir = f'data/api_ergast/{current_date}'
        os.makedirs(new_dir, exist_ok=True)

        # Save the file in the new directory
        df.to_csv(f'{new_dir}/driver_standings.csv', index=False)

        print(f"\n--> File saved in {new_dir} directory")
    else:
        print("Failed to retrieve data")

get_drivers_standings()