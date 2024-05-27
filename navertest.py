import requests
from bs4 import BeautifulSoup


def crawl_naver_news(search_query):
    base_url = "https://search.naver.com/search.naver" 
    params = {"query": search_query, "where": "news"}
    
    response = requests.get(base_url, params=params, headers={'User-agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    
    # for item in soup.select('.sp_nnews .news_wrap .news_area'):
    #     title_tag = item.select_one('.news_tit')
    #     title = title_tag.get_text(strip=True) if title_tag else 'No title'
    #     link = title_tag['href'] if title_tag else 'No link'


    for item in soup.select('div.news_contents'):
        title_tag = item.select_one('.news_tit')

    
        if title_tag:
            title = title_tag.get_text(strip=True)   
            link = title_tag['href']
        
        results.append({'title': title, 'link': link})
    
    i=0

    for item in soup.select('div.info_group'):

        news = item.find('a', class_='info press').text.strip()
        date = item.find('span', class_='info').text.strip()

        results[i]['news'] = news
        results[i]['date'] = date
        
        i += 1

    
    return results


search_query = input("검색어를 입력하세요: ")
naver_results = crawl_naver_news(search_query)



# 네이버 검색 결과 출력
print("네이버 뉴스 검색 결과:")
for result in naver_results:
    print(f"\nTitle: {result['title']}\nLink: {result['link']}\ndate: {result['date']}\nnews : {result['news']}\n")
