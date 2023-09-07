from bs4 import BeautifulSoup
import requests
import openpyxl
from openpyxl import Workbook
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from tqdm import tqdm
from datetime import date, datetime, timedelta


date_list=[]
start_date = datetime(2023,8,30)
end_date = datetime(2023,9,2)

while(start_date<=end_date):
    date_list.append(start_date.strftime("%Y%m%d"))
    start_date+=timedelta(days=1)
#특정 기간동안 존재하는 날짜들을 list로 만들어줌

article_list = []

def url_parsing(date,page):
    url = f"https://news.daum.net/breakingnews/economic?regDate={date}&page={page}"
    return url


def find_links(date,page,arr):
    req_url = requests.get(url_parsing(date,page), headers={"User-Agent": "Mozilla/5.0"\
    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "\
    "Chrome/116.0.5845.96 Safari/537.36"})
    soup = BeautifulSoup(req_url.text, "lxml")

    for i in tqdm(range(0,15)):
        article = soup.select_one(f"#mArticle > div.box_etc > ul > li:nth-child({i+1}) > div > strong > a")
        article_href = article['href']
        arr.append(article_href)

for i in date_list:
    temp=[i]
    for j in range(0,4):
        find_links(i,j+1,temp)
    article_list.append(temp)
#2차원 배열로 만듦. 전체 리스트안에 있는 각각의 리스트는 하루치의 기사의 링크를 담고 있음.
#find_links에 배열을 변수로 받아서 거기에 기사를 추가하고 그 리스트를 다시 article_list에 붙이는 방식임.



print(article_list)
print(len(article_list))
