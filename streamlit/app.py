import streamlit as st
import joblib
import os

# Add a banner at the top 
st.image("https://static.tickets-platform.com/img/pages/39/2131/255/media/1/desktop/image_group-4.jpg?ts=1567173131")

# Add F1 logo top of sidebar
st.sidebar.image("https://1000logos.net/wp-content/uploads/2021/06/F1-logo.png")

# Title of the web app
st.title("Formula 1 Grand Prix Insights")

# Load the ML model
def load_model(model_name):
    # Modify the path to where your model is saved
    model_path = f"Models/{model_name}/model.pkl"
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        return model
    else:
        return None

# Model selector
model_names = os.listdir("Models")
selected_model = st.sidebar.selectbox("Select a model", model_names)

model = load_model(selected_model)

# Check if the model was loaded
if model is not None:

    # User input
    st.write("Enter the weighted position from the last races:")
    weighted_position = st.number_input('Weighted Position', value=0.0, format="%.2f")

    # Predict button
    if st.button('Predict Next Race Position'):
        # Ensure the input is in the expected format
        prediction = model.predict([[weighted_position]])
        st.write(f'Predicted Position Order in Next Race: {prediction[0]:.0f}')
else:
    st.write("Error: Model not found. Please check the model path.")