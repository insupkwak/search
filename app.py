from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)


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


def crawl_daum_news(search_query):
    base_url = "https://search.daum.net/search"
    params = {"nil_suggest": "btn", "w": "news", "DA": "SBC", "q": search_query}
    
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for item in soup.select('strong.tit-g'):
        title_tag = item.select_one('a')
     
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag['href']
        results.append({'title': title, 'link': link})


    i = 0
    for item in soup.select('div.c-tit-doc .area_tit .inner_header'):
        news_tag = item.select_one('a')
        news = news_tag.get_text(strip=True)
        
        results[i]['news'] = news
        i += 1

    i = 0
    for item in soup.select('div.item-contents'):
        date_tag = item.select_one('span.gem-subinfo')
        date = date_tag.get_text(strip=True)
        
        results[i]['date'] = date
        i += 1

    return results


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_news():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query parameter provided"}), 400

    naver_results = crawl_naver_news(query)
    daum_results = crawl_daum_news(query)

    return jsonify({"naver": naver_results, "daum": daum_results})

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=False)
    except Exception as e:
        print("An error occurred while running the server:", e)