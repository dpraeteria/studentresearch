from bs4 import BeautifulSoup
import requests
import openpyxl
from openpyxl import Workbook
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from tqdm import tqdm
from datetime import date, datetime


start_time = int(input('Enter Start Time : '))
end_time = int(input('Enter End Time : '))


# def format_date(input_date):
#     formatted_date = input_date.strftime("%Y%m%d")
#     return formatted_date

article_list = []

def url_parsing(date,page):
    url = f"https://news.daum.net/breakingnews/economic?regDate={date}&page={page}"
    return url


def find_links(date,page):
    global article_list
    req_url = requests.get(url_parsing(date,page), headers={"User-Agent": "Mozilla/5.0"\
    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "\
    "Chrome/116.0.5845.96 Safari/537.36"})
    soup = BeautifulSoup(req_url.text, "lxml")

    for i in tqdm(range(0,15)):
        article = soup.select_one(f"#mArticle > div.box_etc > ul > li:nth-child({i+1}) > div > strong > a")
        article_href = article['href']
        article_list.append(article_href)

for i in range(0,4):
    find_links("20230906",i+1)




print(list(set(article_list)))
print(len(article_list))
