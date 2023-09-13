from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from datetime import datetime, timedelta
from Crawling_Modules import find_last_page, extract_article
import csv
import random

date_list=[]
start_date = datetime(2020,5,8)
end_date = datetime(2020,5,9)

num_page = 8
article_per_page = 8

f=open('article.csv','w',encoding="utf-8-sig",newline='')
write=csv.writer(f)
#csv 파일 실행/생성

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

    for i in range(article_per_page):
        article = soup.select_one(f"#mArticle > div.box_etc > ul > li:nth-child({i+1}) > div > strong > a")
        article_href = article['href']
        links_array.append(article_href)
    return links_array

for date_temp in tqdm(date_list,desc='Days',position=0):
    
    article_daily=[date_temp]
    last_page=find_last_page(date_temp)
    page_list=[] #랜덤으로 뽑은 페이지를 저장할 리스트

    for i in range(num_page): #페이지 8개를 무작위로 뽑음(범위 :1~마지막 페이지)
        page_list.append(random.randint(1,last_page))

    for pages in tqdm(page_list,desc='Pages',position=1,leave=False):#페이지별로 클롤링 및 append, range(시작페이지, 끝 페이지)
        arr=find_links(date_temp,pages)
        for i in tqdm(range(article_per_page),position=2,leave=False):
            article_daily.append(extract_article(arr[i]))
    write.writerow(article_daily)#일별로 기사 row 작성

f.close