import requests
from bs4 import BeautifulSoup



def crawl_daum_news(search_query):
    base_url = "https://search.daum.net/search"
    params = {"nil_suggest": "btn", "w": "news", "DA": "SBC", "q": search_query}
    
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_results = []
    for item in soup.select('strong.tit-g'):
        title_tag = item.select_one('a')
     
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag['href']
        news_results.append({'title': title, 'link': link})


    i=0
    for item in soup.select('div.c-tit-doc .area_tit .inner_header'):
        news_tag = item.select_one('a')
        news = news_tag.get_text(strip=True)
      
        
        news_results[i]['news'] = news
        i += 1

    i=0
    for item in soup.select('div.item-contents'):
            date_tag = item.select_one('span.gem-subinfo')
            date = date_tag.get_text(strip=True)
            
            news_results[i]['date'] = date
            i += 1

    return news_results


search_query = input("검색어를 입력하세요: ")
daum_results = crawl_daum_news(search_query)


# 다음 검색 결과 출력
print("다음 뉴스 검색 결과:")
for result in daum_results:
    print(f"\nTitle: {result['title']}\nLink: {result['link']}\ndate: {result['date']}\nnews : {result['news']}\n")