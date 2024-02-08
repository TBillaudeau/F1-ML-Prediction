# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# import chromedriver_autoinstaller_fix


# import time

# def test_main():
#     # Create a new instance of the Firefox driver
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")

#     chromedriver_autoinstaller_fix.install()  
#     driver = webdriver.Chrome(options=chrome_options)

#     # Go to your app's URL
#     driver.get("https://efrei--streamlit--4f4tjmnqvxl8.code.run/")  # replace with your app's URL

#     # Wait for the predict button to be present
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Predict Finishing Position 🚀")]')))

#     # Test the title
#     assert "F1 Grand Prix Prediction" in driver.page_source

#     # Test the sidebar
#     assert "Select a model" in driver.page_source

#     # Test the user input
#     assert "Select Constructor" in driver.page_source
#     assert "Select Driver" in driver.page_source

#     # Test the predict button
#     assert "Predict Finishing Position 🚀" in driver.page_source

#     # Close the browser window
#     driver.quit()

# if __name__ == "__main__":
#     test_main()