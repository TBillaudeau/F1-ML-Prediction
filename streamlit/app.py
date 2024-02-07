import streamlit as st
import pandas as pd
import joblib
import glob
import os

# Set up the page
def setup_page():
    st.set_page_config(page_title="F1 Grand Prix Prediction", page_icon="🏎️", initial_sidebar_state="expanded")
    st.title(":red[Formula 1] Grand Prix Prediction")
    st.image("https://static.tickets-platform.com/img/pages/39/2131/255/media/1/desktop/image_group-4.jpg")
    hide_streamlit_style()

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

# Get most recent directory
def get_most_recent_dir(path):
    path_pattern = os.path.join(path)
    directories = glob.glob(path_pattern)
    most_recent_dir = max(directories, key=os.path.getmtime)
    return most_recent_dir

# Model selection
def load_model(model_name):
    model_path = f"../Models/{model_name}/random_forest_regressor_model.pkl"
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        return None

# Sidebar
def sidebar():
    st.sidebar.image("https://1000logos.net/wp-content/uploads/2021/06/F1-logo.png")
    model_names = os.listdir("../Models")
    selected_model = st.sidebar.selectbox("Select a model", model_names, index=0)
    return selected_model

# Load data
def load_data():
    constructor_data = pd.read_csv(get_most_recent_dir("../data/api_ergast/*") + '/constructors.csv')
    driver_data = pd.read_csv(get_most_recent_dir("../data/api_ergast/*") + '/drivers.csv')
    race_data = pd.read_csv(get_most_recent_dir("../data/api_ergast/*") + '/races.csv')
    return constructor_data, driver_data, race_data

# User input
def get_user_data(constructor_data, driver_data, race_data):
    constructor_dict = {f"{row['name']}": row['constructorId'] for _, row in constructor_data.iterrows()}
    driver_dict = {f"{row['forename']} {row['surname']}": row['driverId'] for _, row in driver_data.iterrows()}
    race_dict = {f"{row['name']}": row['raceId'] for _, row in race_data.iterrows()}

    selected_constructor_name = st.selectbox('Select Constructor', options=list(constructor_dict.keys()), index=5)
    selected_driver_name = st.selectbox('Select Driver', options=list(driver_dict.keys()), index=842)
    selected_race_name = st.selectbox('Select Race', options=list(race_dict.keys()), index=5)
    grid_position = st.number_input('Enter Grid Position', value=3, min_value=1, max_value=20, step=1)

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
        st.metric(label="", value=predictions[0])
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
            with col3:
                st.write("e")
                
if __name__ == "__main__":
    main()