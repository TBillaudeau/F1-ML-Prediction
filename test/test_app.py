from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_main():
    # Create a new instance of the Firefox driver
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)

    # Go to your app's URL
    driver.get("https://efrei--streamlit--4f4tjmnqvxl8.code.run/")  # replace with your app's URL

    # Wait for the predict button to be present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Predict Finishing Position 🚀")]')))

    # Test the title
    assert "F1 Grand Prix Prediction" in driver.page_source

    # Test the sidebar
    assert "Select a model" in driver.page_source

    # Test the user input
    assert "Select Constructor" in driver.page_source
    assert "Select Driver" in driver.page_source

    # Test the predict button
    assert "Predict Finishing Position 🚀" in driver.page_source

    # Close the browser window
    driver.quit()

if __name__ == "__main__":
    test_main()