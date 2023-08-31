from bs4 import BeautifulSoup
import requests
import openpyxl
from openpyxl import Workbook
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from tqdm import tqdm

def url_parsing(page , date):
    url = f"https://www.google.com/search?q=경제+뉴스&tbm=nws&tbs=cdr:1,cd_min:{date},cd_max:{date}&start={50*(page-1)}"
    return url

req_url = requests.get(url_parsing(1,"8/30/2023"), headers={"User-Agent": "Mozilla/5.0"\
    "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "\
    "Chrome/116.0.5845.96 Safari/537.36"})

soup = BeautifulSoup(req_url.text, "lxml")
def find_a():
    # a_tag = soup.find_all("a")
    tag_lst = []
    for i in tqdm(range(50)):
        article_element = soup.select_one(f'div.SoaBEf > div > div > a')
        # article['']
        if article_element != None:
            tag_lst.append(article_element['href'])
        else:
            continue
    return tag_lst
    
#################################DEEP 한 요소 추출################################
#rso > div > div > div:nth-child(1) > div > div > a > div > div.iRPxbe > div.n0jPhd.ynAwRc.MBeuO.nDgy9d
#rso > div > div > div:nth-child(2) > div > div > a > div > div.iRPxbe > div.n0jPhd.ynAwRc.MBeuO.nDgy9d
##마지막 : 

################################링크 추출########################################
#rso > div > div > div:nth-child(1) > div > div > a

# url = url_parsing(1,"8/30/2023")

print(find_a())
print(f'\n\n 길이 : {len(find_a())}')
