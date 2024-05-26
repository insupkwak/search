import requests
from bs4 import BeautifulSoup


def crawl_naver_news(search_query):
    base_url = "https://search.naver.com/search.naver"
    params = {"query": search_query, "where": "news"}
    
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    
    for item in soup.select('.sp_nnews .news_wrap .news_area'):
        title_tag = item.select_one('.news_tit')
        title = title_tag.get_text(strip=True) if title_tag else 'No title'
        link = title_tag['href'] if title_tag else 'No link'
        
        # 각 뉴스 기사에 대해 날짜 정보를 가져옴
        info_span = item.select_one('span.info')
        info_text = info_span.get_text(strip=True) if info_span else 'No date'
        
        # 추가 정보 가져오기
        news_div = item.select_one('div.info_group')
        news_info_span = news_div.select_one('.info.press')
        news_info = news_info_span.get_text(strip=True) if news_info_span else 'No news info'
        
        results.append({'title': title, 'link': link, 'date': info_text, 'news': news_info})
    
    return results


search_query = input("검색어를 입력하세요: ")
naver_results = crawl_naver_news(search_query)



# 네이버 검색 결과 출력
print("네이버 뉴스 검색 결과:")
for result in naver_results:
    print(f"\nTitle: {result['title']}\nLink: {result['link']}\ndate: {result['date']}\nnews : {result['news']}\n")
