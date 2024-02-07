import streamlit as st
import joblib
import os
import glob
import pandas as pd


# Add a banner at the top 
st.image("https://static.tickets-platform.com/img/pages/39/2131/255/media/1/desktop/image_group-4.jpg?ts=1567173131")

# Add F1 logo top of sidebar
st.sidebar.image("https://1000logos.net/wp-content/uploads/2021/06/F1-logo.png")

# Title of the web app
st.title("Formula 1 Grand Prix Insights")

def get_most_recent_dir():
    path_pattern = os.path.join("../Models", "*")
    directories = glob.glob(path_pattern)
    most_recent_dir = max(directories, key=os.path.getmtime)
    return most_recent_dir 

def load_model():
    path = get_most_recent_dir()
    model_path = f"{path}/random_forest_regressor_model.pkl"
    print("Model path: ", model_path)
    print("File exists: ", os.path.exists(model_path))
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        return model
    else:
        st.error("Model file does not exist: " + model_path)
        return None

model = load_model()

# Add form elements to get user input
grid = st.sidebar.number_input('Grid position', min_value=1, max_value=20, value=1)
constructorId = st.sidebar.number_input('Constructor ID', min_value=1, max_value=100, value=1)
driverId = st.sidebar.number_input('Driver ID', min_value=1, max_value=1000, value=1)
circuitId = st.sidebar.number_input('Circuit ID', min_value=1, max_value=100, value=1)

# Example new data for prediction
# Suppose you want to predict the finishing position for a driver starting from grid position 5 for constructor ID 1
new_data = {
    'grid': [grid],  # Grid position
    'constructorId': [constructorId],  # Constructor ID
    'driverId': [driverId],  # Driver ID
    'circuitId': [circuitId]
}
st.markdown("### For example try with: ")
st.markdown("* Grid position: 1")
st.markdown("* Constructor ID: 9")
st.markdown("* Driver ID: 830")
st.markdown("* Circuit ID: 6")

# Convert the new data to a DataFrame
new_data_df = pd.DataFrame(new_data)

# Use the model to make predictions
predictions = model.predict(new_data_df)

# Print the predicted finishing position
st.write(f"Predicted Finishing Position: {predictions[0]}")