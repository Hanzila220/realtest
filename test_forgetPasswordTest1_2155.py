import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd
import datetime

# CSV file path to store all test results
CSV_FILE_PATH = "test_results.csv"

class TestForgetPasswordTest:
    def setup_method(self, method):
        # Set up headless Chrome options for CI
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1296, 696)

        # Ensure screenshots directory exists
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

    def teardown_method(self, method):
        # Close the browser after each test
        self.driver.quit()

    def append_to_csv(self, results):
        """Append the test results to the CSV file."""
        if not os.path.exists(CSV_FILE_PATH):
            df = pd.DataFrame(results)
            df.to_csv(CSV_FILE_PATH, index=False)  # Write a new file if it doesn't exist
        else:
            df = pd.DataFrame(results)
            df.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)  # Append to existing file

    def test_forget_password(self):
        start_time = time.time()

        # Navigate to the login page
        self.driver.get("https://smoothmaths.co.uk/login/")
        
        # Click on the 'Forgot Password' link
        self.driver.find_element(By.LINK_TEXT, "Forgot Password").click()

        # Enter the email or username to request a password reset
        self.driver.find_element(By.ID, "mepr_user_or_email").send_keys("Testing")  
        self.driver.find_element(By.ID, "wp-submit").click()

        # Wait for the success message to appear
        try:
            success_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.mepr_password_reset_requested h3"))
            )
            assert "Successfully requested password reset" in success_message.text, "Expected success message not found."

            # Take a screenshot of the success message
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"screenshots/password_reset_{timestamp}.png"
            self.driver.save_screenshot(screenshot_path)

            status = "Passed"

        except Exception as e:
            status = "Failed"
            screenshot_path = None

        # Record end time and calculate duration
        end_time = time.time()
        duration = end_time - start_time

        # Prepare results for CSV
        results = {
            "Test Case": ["Test Forget Password"],
            "Status": [status],
            "Duration (seconds)": [round(duration, 2)],
            "Screenshot": [screenshot_path]
        }

        # Append results to the CSV file
        self.append_to_csv(results)
