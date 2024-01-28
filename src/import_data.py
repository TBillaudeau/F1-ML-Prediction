import requests
import pandas as pd
import os

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
        print(df.head(2))

        df.to_csv(f'data/api_ergast/driver_standings.csv', index=False)
    else:
        print("Failed to retrieve data")

get_drivers_standings()