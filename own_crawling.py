from bs4 import BeautifulSoup
import requests
import openpyxl
from openpyxl import Workbook
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from tqdm import tqdm
from datetime import date, datetime, timedelta
import numpy as np


date_list=[]
start_date = datetime(2023,8,31)
end_date = datetime(2023,9,1)


######헤더 너무 길어서 보기 불편해서 따로 꺼내놓음######
header = {"User-Agent": "Mozilla/5.0"\
    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "\
    "Chrome/116.0.5845.96 Safari/537.36"}


while(start_date<=end_date):
    date_list.append(start_date.strftime("%Y%m%d"))#날짜형식 : YYYYMMDD
    start_date+=timedelta(days=1)
#특정 기간동안 존재하는 날짜들을 list로 만들어줌

article_list = []


url_parsing = lambda date,page : f"https://news.daum.net/breakingnews/economic?regDate={date}&page={page}"

def extract_article(link):
    soup = BeautifulSoup(requests.get(link, headers=header).text, "lxml")
    p_tags = soup.findAll("p")
    article = "\n".join([p.get_text() for p in p_tags])  # 각 p 태그의 텍스트를 추출하고 개행 문자로 연결
    return article        

print(article_list)


def find_links(date,page,arr):
    global header
    req_url = requests.get(url_parsing(date,page), headers=header)
    soup = BeautifulSoup(req_url.text, "lxml")

    for i in tqdm(range(0,15)):
        article = soup.select_one(f"#mArticle > div.box_etc > ul > li:nth-child({i+1}) > div > strong > a")
        article_href = article['href']
        arr.append(article_href)

for i in date_list:
    temp=[i]
    for j in range(0,4):
        find_links(i,j+1,temp)
    article_list.append(list(set(temp)))


print(article_list)
print(np.size(article_list)) # 크롤링된 기사의 개수