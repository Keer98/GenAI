This project scrapes job listings related to Generative AI (Gen AI) from Dice.com and saves the extracted information to a CSV file named gen_ai_job_list.csv.

Requirements:

Python 3.x
Libraries:
Selenium
webdriver_manager
csv
Installation:

Install the required libraries using pip:
Bash
pip install selenium webdriver_manager csv
Use code with caution.

Usage:

Open a terminal and navigate to the directory containing this project's files.
Run the script:
Bash
python gen_ai_job_list_scraper.py
Use code with caution.

This will start scraping and save extracted data to gen_ai_job_list.csv.

Output:

The script creates a CSV file named gen_ai_job_list.csv containing the following data points for each job listing (up to 100 listings):

Job Title
Company
Location
Required Skills (extracted from job description)
Kind of Job (full-time, part-time, etc.)
Posted On

