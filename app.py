from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import datetime


app = Flask(__name__)

discord = "https://discord.com/api/webhooks/1176157989506404512/MPNnjvAJdhmsY37AGexHLQDwgUnekpRSRQKTWHC8_3PMQwrq1u0Z_wB_bR_b1BZHqnSx"

#메시지 전송
def send_message(msg):
    now = datetime.datetime.now()
    message = {"content": f"[{now.strftime('%H:%M')}] {str(msg)}"}
    requests.post(discord, data=message)


def crawl_naver_news(search_query):

    base_url = "https://search.naver.com/search.naver"
    params = {"query": search_query, "where": "news"}
     
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    
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