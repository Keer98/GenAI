import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import warnings

warnings.filterwarnings("ignore")

def scrape_website(base_url):
    """Scrapes the website starting from the base URL."""
    visited_urls = set()
    website_content = []

    def scrape_page(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text(separator=" ", strip=True)
            website_content.append({"url": url, "content": page_text})

            for link in soup.find_all('a', href=True):
                full_url = urljoin(base_url, link['href'])
                if base_url in full_url and full_url not in visited_urls:
                    visited_urls.add(full_url)
                    scrape_page(full_url)

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    scrape_page(base_url)
    return website_content
