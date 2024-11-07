import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# Initialize WebDriver (with automatic ChromeDriver setup)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Define the initial URL for scraping
base_url = 'https://www.dice.com/jobs?q=Gen%20AI%20Developer&countryCode=US&radius=30&radiusUnit=mi&pageSize=20&language=en'
driver.get(base_url)

# Open a CSV file to store the data
with open('gen_ai_job_list.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['Job Title', 'Company', 'Location', 'Required Skills', 'Kind of Job', 'Posted On'])

    def scrape_page():
        job_cards = driver.find_elements(By.CLASS_NAME, 'card')  # Check if 'card' is the correct class name
        print(f"Found {len(job_cards)} job cards on this page.")
        
        for card in job_cards:
            try:
                title = card.find_element(By.CLASS_NAME, 'card-title-link').text.strip()
            except:
                title = 'Not available'
            
            try:
                company = card.find_element(By.CSS_SELECTOR, '.card-company span').text.strip()
            except:
                company = 'Not available'

            try:
                location = card.find_element(By.CSS_SELECTOR, '.card-location span').text.strip()
            except:
                location = 'Not available'

            try:
                job_type = card.find_element(By.CLASS_NAME, 'type').text.strip()
            except:
                job_type = 'Not specified'

            try:
                posted_on = card.find_element(By.CLASS_NAME, 'posted').text.strip()
            except:
                posted_on = 'Not available'

            try:
                description = card.find_element(By.CLASS_NAME, 'card-description').text.strip()
            except:
                description = 'Not available'

            writer.writerow([title, company, location, description, job_type, posted_on])
            print(f"Scraped: {title} at {company}, {location}")

    def scroll_to_element(element):
        driver.execute_script("arguments[0].scrollIntoView(true);", element)

    page_number = 1
    while (page_number<=5):
        print(f"Scraping page {page_number}...")
        time.sleep(3)

        scrape_page()

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'li.pagination-next a.page-link')
            next_button_class = driver.find_element(By.CSS_SELECTOR, 'li.pagination-next').get_attribute('class')

            if 'disabled' in next_button_class:
                print("No more pages to scrape. Exiting.")
                break
            else:
                scroll_to_element(next_button)
                ActionChains(driver).move_to_element(next_button).click().perform()  # Scroll and click
                page_number += 1
        except Exception as e:
            print(f"Exception occurred: {e}. No next button found. Exiting.")
            break

# Close the WebDriver
driver.quit()

print("Scraping completed. Data has been saved to gen_ai_jobs.csv")
