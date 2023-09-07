from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from datetime import datetime, timedelta
from Crawling_Modules import find_last_page, extract_article, flatten_list


article_list = []
date_list=[]
start_date = datetime(2023,8,31)
end_date = datetime(2023,9,1)


while(start_date<=end_date):
    date_list.append(start_date.strftime("%Y%m%d"))#날짜형식 : YYYYMMDD
    start_date+=timedelta(days=1)
#특정 기간동안 존재하는 날짜들을 list로 만들어줌


######헤더 너무 길어서 보기 불편해서 따로 꺼내놓음######
header = {"User-Agent": "Mozilla/5.0"\
    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "\
    "Chrome/116.0.5845.96 Safari/537.36"}






url_parsing = lambda date,page : f"https://news.daum.net/breakingnews/economic?regDate={date}&page={page}"


##링크들을 추출하는 함수
def find_links(date : int,page : int) -> list:
    links_array = []
    global header
    req_url = requests.get(url_parsing(date,page), headers=header)
    soup = BeautifulSoup(req_url.text, "lxml")

    for i in tqdm(range(0,15)):
        article = soup.select_one(f"#mArticle > div.box_etc > ul > li:nth-child({i+1}) > div > strong > a")
        article_href = article['href']
        links_array.append(article_href)
    return links_array


for date_temp in date_list:
    article_daily=[date_temp]
    for pages in tqdm(range(1,5)):
        arr=list(set(find_links(date_temp,pages)))
        for i in range(15):
            article_daily.append(extract_article(arr[i]))
    article_list.append(article_daily)

print(article_list)