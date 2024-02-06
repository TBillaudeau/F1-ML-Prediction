# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np

# Add a banner at the top 
st.image("https://static.tickets-platform.com/img/pages/39/2131/255/media/1/desktop/image_group-4.jpg?ts=1567173131")

# Add F1 logo top of sidebar
st.sidebar.image("https://1000logos.net/wp-content/uploads/2021/06/F1-logo.png")

# Title of the web app
st.title("Formula 1 Grand Prix Insights")


def import_all_data():
    path = "data/Formula 1 World Championship (1950 - 2023) Kaggle"

    # ----- Load data from csv files -----

    # circuitId,circuitRef,name,location,country,lat,lng,alt,url
    df_circuits = pd.read_csv(path + "/circuits.csv")

    # constructorResultsId,raceId,constructorId,points,status
    df_constructor_results = pd.read_csv(path + "/constructor_results.csv")

    # constructorStandingsId,raceId,constructorId,points,position,positionText,wins
    df_constructor_standings = pd.read_csv(path + "/constructor_standings.csv")

    # data/Formula 1 World Championship (1950 - 2023) Kaggle/constructors.csv
    df_constructors = pd.read_csv(path + "/constructors.csv")

    # driverStandingsId,raceId,driverId,points,position,positionText,wins
    df_driver_standings = pd.read_csv(path + "/driver_standings.csv")

    # driverId,driverRef,number,code,forename,surname,dob,nationality,url
    df_drivers = pd.read_csv(path + "/drivers.csv")

    # raceId,driverId,lap,position,time,milliseconds
    df_lap_times = pd.read_csv(path + "/lap_times.csv")

    # raceId,driverId,stop,lap,time,duration,milliseconds
    df_pit_stops = pd.read_csv(path + "/pit_stops.csv")

    # qualifyId,raceId,driverId,constructorId,number,position,q1,q2,q3
    df_qualifying = pd.read_csv(path + "/qualifying.csv")

    # raceId,year,round,circuitId,name,date,time,url,fp1_date,fp1_time,fp2_date,fp2_time,fp3_date,fp3_time,quali_date,quali_time,sprint_date,sprint_time
    df_races = pd.read_csv(path + "/races.csv")

    # resultId,raceId,driverId,constructorId,number,grid,position,positionText,positionOrder,points,laps,time,milliseconds,fastestLap,rank,fastestLapTime,fastestLapSpeed,statusId
    df_results = pd.read_csv(path + "/results.csv")

    # year,url
    df_seasons = pd.read_csv(path + "/seasons.csv")

    # resultId,raceId,driverId,constructorId,number,grid,position,positionText,positionOrder,points,laps,time,milliseconds,fastestLap,fastestLapTime,statusId
    df_sprint_results = pd.read_csv(path + "/sprint_results.csv")

    # statusId,status
    df_status = pd.read_csv(path + "/status.csv")

    return df_circuits, df_constructor_results, df_constructor_standings, df_constructors, df_driver_standings, df_drivers, df_lap_times, df_pit_stops, df_qualifying, df_races, df_results, df_seasons, df_sprint_results, df_status

# Import data
df_circuits, df_constructor_results, df_constructor_standings, df_constructors, df_driver_standings, \
df_drivers, df_lap_times, df_pit_stops, df_qualifying, df_races, df_results, \
df_seasons, df_sprint_results, df_status = import_all_data()

# Change types
# Set col date from df_races to datetime (format : 2009-03-29)
df_races['date'] = pd.to_datetime(df_races['date'], format='%Y-%m-%d')

# ----- Create sidebar selectboxes -----
# Extract unique seasons and sort them in descending order
unique_seasons = np.sort(df_seasons['year'].unique())[::-1]

# Create a sidebar selectbox for the seasons
selected_season = st.sidebar.selectbox('Select a Season', unique_seasons)


# ----- Main frame -----
# Show a table of the list of all races for this season
st.subheader("List of all races for this season")
st.dataframe(df_races[df_races['year'] == selected_season])


