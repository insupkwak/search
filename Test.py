from bs4 import BeautifulSoup
import requests
import re
import urllib.parse

def crawl_google_news(query):
    url = f"https://www.google.com/search?q={query}&tbm=nws"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_results = []

    for result in soup.find_all('div', class_='Gx5Zad'):
        title_elem = result.find('div', class_='BNeawe')
        if title_elem:
            news = {}
            news['title'] = title_elem.text

            link_elem = result.find('a')
            if link_elem:
                # Extracting the link and removing unnecessary parameters
                link = link_elem['href']
                # Decoding the URL to handle special characters like "&amp;"
                decoded_link = urllib.parse.unquote(link)
                match = re.search(r'(https?://[^&]+)', decoded_link)
                if match:
                    news['link'] = match.group(1)


            date_elem = result.find('span', class_='r0bn4c')
            news['date'] = date_elem.text if date_elem else None

            content_elem = result.find('div', class_='BNeawe UPmit AP7Wnd lRVwie')
            news['news'] = content_elem.text if content_elem else None

            if not news['news']:  # If news is None, try to scrape the next article
                continue

            news_results.append(news)

    return news_results



query = input("검색어를 입력하세요: ")
results = crawl_google_news(query)

# If no news found, try to scrape the next article
if not results:
    print("No news found. Scraping next article.")
    next_query = "다음 기사 " + query
    results = crawl_google_news(next_query)

# Print search results
print("뉴스 검색 결과:")
for result in results:
    print(f"\nTitle: {result['title']}\nLink: {result['link']}\nDate: {result['date']}\nNews: {result['news']}\n")