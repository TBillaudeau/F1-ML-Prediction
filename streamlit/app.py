import streamlit as st
import pandas as pd
import joblib
import glob
import os

global pre_path
pre_path = "../"

# Set up the page
def setup_page():
    st.set_page_config(page_title="F1 Grand Prix Prediction", page_icon="🏎️", initial_sidebar_state="expanded")
    st.title(":red[Formula 1] Grand Prix Prediction")
    st.caption("A project proposed by Khodor Hammoud - Efrei Paris")
    st.image("https://static.tickets-platform.com/img/pages/39/2131/255/media/1/desktop/image_group-4.jpg")
    # hide_streamlit_style()

# Hide Streamlit style
def hide_streamlit_style():
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .css-1y4p8pa {padding: 2rem 1rem 0rem;}
        </style>
        """
    st.markdown(hide_st_style, unsafe_allow_html=True)

def get_stats_from_dataset():
    # Get drivers
    df_drivers = pd.read_csv(get_most_recent_dir(f"{pre_path}data/Formula 1 World Championship (1950 - 2023) Kaggle/drivers.csv"))
    nbr_drivers = len(df_drivers)
    # Get constructors
    df_constructors = pd.read_csv(get_most_recent_dir(f"{pre_path}data/Formula 1 World Championship (1950 - 2023) Kaggle/constructors.csv"))
    nbr_constructors = len(df_constructors)
    # Get races
    df_races = pd.read_csv(get_most_recent_dir(f"{pre_path}data/Formula 1 World Championship (1950 - 2023) Kaggle/races.csv"))
    nbr_races = len(df_races)
    # Get circuits
    df_circuits = pd.read_csv(get_most_recent_dir(f"{pre_path}data/Formula 1 World Championship (1950 - 2023) Kaggle/circuits.csv"))
    nbr_circuits = len(df_circuits)
    return nbr_drivers, nbr_constructors, nbr_races, nbr_circuits

# Get most recent directory
def get_most_recent_dir(path):
    directories = glob.glob(path)
    most_recent_dir = max(directories, key=os.path.getmtime)
    return most_recent_dir

# Model selection
def load_model(model_name):
    model_path = f"{pre_path}Models/{model_name}/random_forest_regressor_model.joblib"
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        return None

# Sidebar
def sidebar():
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/F1.svg/2560px-F1.svg.png")
    model_names = os.listdir(f"{pre_path}Models")
    model_names.sort(key=lambda x: os.path.getmtime(f"{pre_path}Models/" + x), reverse=True)
    selected_model = st.sidebar.selectbox("Select a model", model_names, index=0)
    st.sidebar.divider()

    # Add stats
    st.sidebar.subheader("Main stats")
    nbr_drivers, nbr_constructors, nbr_races,nbr_circuits = get_stats_from_dataset()

    col1, col2 = st.sidebar.columns(2)
    # Drivers
    col1.metric(label="Drivers", value=nbr_drivers)
    col2.metric(label="", value="👨‍✈️")

    # Constructors
    col1.metric(label="Constructors", value=nbr_constructors)
    col2.metric(label="", value="🏎️")

    # Races
    col1.metric(label="Races", value=nbr_races)
    col2.metric(label="", value="🏁")

    # Circuits
    col1.metric(label="Circuits", value=nbr_circuits)
    col2.metric(label="", value="🌍")

    st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Logo_Efrei_2022.svg/1280px-Logo_Efrei_2022.svg.png")

    return selected_model

# Load data
def load_data():
    print()
    constructor_data = pd.read_csv(get_most_recent_dir(f"{pre_path}data/api_ergast/*") + '/constructors.csv')
    driver_data = pd.read_csv(get_most_recent_dir(f"{pre_path}data/api_ergast/*") + '/drivers.csv')
    race_data = pd.read_csv(get_most_recent_dir(f"{pre_path}data/api_ergast/*") + '/races.csv')
    return constructor_data, driver_data, race_data

# User input
def get_user_data(constructor_data, driver_data, race_data):
    constructor_dict = {f"{row['name']}": row['constructorId'] for _, row in constructor_data.iterrows()}
    driver_dict = {f"{row['forename']} {row['surname']}": row['driverId'] for _, row in driver_data.iterrows()}
    race_dict = {f"{row['name']}": row['raceId'] for _, row in race_data.iterrows()}

    selected_constructor_name = st.selectbox('Select Constructor', options=list(constructor_dict.keys()), index=5)
    selected_driver_name = st.selectbox('Select Driver', options=list(driver_dict.keys()), index=842)
    selected_race_name = "Monaco Grand Prix"
    grid_position = st.slider('Grid Position', min_value=1, max_value=20, value=10, step=1)

    return selected_constructor_name, selected_driver_name, selected_race_name, grid_position, constructor_dict, driver_dict, race_dict

def predict_position(model, grid_position, constructorId, driverId, circuitId):
    if model:
        new_data_df = pd.DataFrame({
            'grid': [grid_position],
            'constructorId': [constructorId],
            'driverId': [driverId],
            'circuitId': [circuitId]
        })
        predictions = model.predict(new_data_df)
        # Reduce to int
        predictions = [int(x) for x in predictions]
        st.metric(label="Prediction is", value=f"{predictions[0]}th", delta=(predictions[0] - grid_position)*-1, delta_color="normal")
    else:
        st.error("Model not loaded. Please check the model path and try again.")

# Main app function
def main():
    setup_page()
    constructor_data, driver_data, race_data = load_data()
    selected_model = sidebar()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("User Input")
        selected_constructor_name, selected_driver_name, selected_race_name, grid_position, constructor_dict, driver_dict, race_dict = get_user_data(constructor_data, driver_data, race_data)
        model = load_model(selected_model)
    if st.button('Predict Finishing Position 🚀'):
        with col2:
            st.subheader("Position")
            col1, col2, col3 = st.columns(3)
            with col2:
                predict_position(model, grid_position, constructor_dict[selected_constructor_name], driver_dict[selected_driver_name], race_dict[selected_race_name])

    st.markdown("<br>", unsafe_allow_html=True)
    # More informations on the project
    with st.expander("❓ About the project"):
        st.write("This project is a part of the Efrei Paris Data Science course. The goal is to predict the finishing position of a driver in a Formula 1 Grand Prix. The data used for this project is from the Kaggle dataset: [Formula 1 World Championship (1950 - 2023)](https://www.kaggle.com/rohanrao/formula-1-world-championship-1950-2020) and the [Ergast API](http://ergast.com/mrd/).")
        st.write("One important note is how the results can seems to be not accurate sometimes. This is due to the fact that predicting the outcome of a F1 race is a very complex task. There are many factors that can influence the outcome of a race. For example, the weather, the track conditions ...")
        st.write("Thank you for using our app and we hope you enjoyed it!")
    
    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("Made with ❤️ by **ARBEY** Louis, **BILLAUDEAU** Thomas and **CRETINON** Pierre-Louis")
    st.link_button("👨‍💻 Github repository", "https://github.com/TBillaudeau/F1-ML-Prediction")
if __name__ == "__main__":
    main()