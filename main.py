import requests
from bs4 import BeautifulSoup
import csv
import re

def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def parse_news_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    results = soup.find(class_='bbc-k6wdzo')
    if not results:
        print("No results found.")
        return []

    new_elements = results.find_all("div", class_="promo-text")
    news_items = []

    for new_element in new_elements:
        title_element = new_element.find("h2", class_="bbc-145rmxj e47bds20")
        date_element = new_element.find("time", class_="promo-timestamp bbc-11pkra2 e1mklfmt0")
        
        if title_element and date_element:
            # Clean up the title
            title = re.sub(r'ဗီဒီယို, ', '', title_element.text.strip())
            title = re.sub(r'ကြာမြင့်ချိန်.*', '', title).strip(', ')
            
            news_item = {
                'title': title,
                'date': date_element.text.strip()
            }
            news_items.append(news_item)
    return news_items

def write_to_csv(filename, data, columns):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            for item in data:
                writer.writerow(item)
    except IOError as e:
        print(f"I/O error: {e}")

if __name__ == "__main__":
    url = 'https://www.bbc.com/burmese/topics/c404v08p1wxt'
    content = fetch_page_content(url)
    
    if content:
        news_items = parse_news_content(content)
        
        if news_items:
            csv_file = 'scraped_news.csv'
            csv_columns = ['title', 'date']
            write_to_csv(csv_file, news_items, csv_columns)
            print(f"Data has been written to {csv_file}")
        else:
            print("No news items found.")
    else:
        print("Failed to retrieve the page content.")
