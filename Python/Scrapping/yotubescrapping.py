import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Uncomment this if you want to run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scroll_to_load_comments(driver, timeout=300):
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    start_time = time.time()
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        if time.time() - start_time > timeout:
            print("Timeout reached while scrolling")
            break

def extract_comments(driver):
    comments = []
    comment_elements = driver.find_elements(By.CSS_SELECTOR, 'ytd-comment-thread-renderer #content-text')
    for element in comment_elements:
        comments.append(element.text)
    return comments

def save_to_csv(comments, filename='youtube_comments.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Comment'])
        for comment in comments:
            writer.writerow([comment])

def scrape_youtube_comments(video_url):
    driver = setup_driver()
    try:
        driver.get(video_url)
        
        # Wait for the video player to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'movie_player')))
        
        # Scroll down to load comments section
        driver.execute_script("window.scrollTo(0, 500);")
        
        # Wait for the comments section to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ytd-comments')))
        
        # Scroll to load more comments
        scroll_to_load_comments(driver)
        
        # Extract comments
        comments = extract_comments(driver)
        
        # Save comments to CSV
        save_to_csv(comments)
        
        print(f"Scraped {len(comments)} comments and saved them to youtube_comments.csv")
    except TimeoutException:
        print("Timeout while waiting for page elements to load")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=qUW6T-1YjPY&lc=Ugxpwj0b2EbvKJCTpbF4AaABAg"  # Replace with your desired video URL
    scrape_youtube_comments(video_url)