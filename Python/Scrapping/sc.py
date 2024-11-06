from selenium import webdriver
# Initialize the Selenium WebDriver (make sure to have the right driver version for your browser)
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from bs4 import BeautifulSoup
import csv  # Import the csv module
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException



# Initialize WebDriver (with automatic ChromeDriver setup)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the website
url = "https://ceoaperolls.ap.gov.in/AP_MLC_2024/ERO/Status_Update_2024/knowYourApplicationStatus.aspx"
driver.get(url)
time.sleep(3)

# *** New line to find the "Graduate" tab ***
graduate_tab = driver.find_element(By.CSS_SELECTOR, "a[href='#Graduate']")

# *** New line to click the "Graduate" tab ***
graduate_tab.click()
# Wait for the page to load (adjust sleep time if needed)
time.sleep(3)


# Select the radio button "teachersEWAPPID"
radio_button = driver.find_element(By.ID, "teachersEWAPPID")
radio_button.click()

# Open the CSV file in append mode
'''with open('application_status.csv', mode='a', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Loop through the range of application IDs
    for i in range(1, 10):  # From 1 to 500
        app_id = f"F19-{i:07d}"  # Format the application ID
        
        # Retry logic for locating elements
        for attempt in range(3):  # Try up to 3 times
            try:
                # Re-locate the search box for each iteration
                search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "txtSearch")))
                search_box.clear()  # Clear the search box
                search_box.send_keys(app_id)  # Enter the application ID in the search box

                # Click the search button
                search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnTeachersEW")))
                search_button.click()

                # Wait for the results to load
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))  # Wait for the table to appear

                # Get the page source after search results load
                page_source = driver.page_source

                # Use BeautifulSoup to parse the HTML content
                soup = BeautifulSoup(page_source, 'html.parser')

                # Find the table or the relevant data container on the page
                data_table = soup.find('table')  # You might need to adjust this selector based on the page's HTML structure

                # Extract rows and columns from the table
                rows = data_table.find_all('tr')

                # Loop through each row and extract the table data
                for row in rows:
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]  # Get rid of any extra spaces
                    if cols:  # Only write non-empty rows
                        csv_writer.writerow(cols)  # Write the row to the CSV file

                break  # Exit the retry loop if successful
            except (StaleElementReferenceException, NoSuchElementException) as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == 2:  # If it's the last attempt, raise the exception
                    raise
            time.sleep(5)

# Close the browser
driver.quit()

print("Data extracted and saved to 'application_status.csv'")'''
