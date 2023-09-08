import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from bs4 import BeautifulSoup

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36"}

url_parsing = lambda date, page:f"https://news.daum.net/breakingnews/economic?regDate={date}&page={page}"

def check_page(date : int, i : int):
    req = requests.get(url_parsing(date, i+1), headers=header)
    if req.text == requests.get(url_parsing(date, i), headers=header).text and i != 0:
        return i
    return None

def find_last_page(date : int):
    req_url = requests.get(url_parsing(date,1000), headers=header)
    soup = BeautifulSoup(req_url.text, "lxml")
    return int(soup.select(f"#mArticle > div.box_etc > div.paging_news > span.inner_paging > a.num_page")[-1].contents[0])+1
#특정 날짜의 마지막 기사 페이지 찾는거 최적화
#만약 300페이지 까지 밖에 없는데 1000페이지를 요청하면 자동으로 맨 마지막 페이지로 다이렉트됨을 이용함


##링크에서 기사를 추출하는 함수
def extract_article(link : str) -> str :
        header = {"User-Agent": "Mozilla/5.0"\
                "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "\
                "Chrome/116.0.5845.96 Safari/537.36"}
        soup = BeautifulSoup(requests.get(link, headers=header).text, "lxml")
        p_tags = soup.findAll("p",attrs={"dmcf-ptype" : "general"})
        article = "\n".join([p.get_text() for p in p_tags])  # 각 p 태그의 텍스트를 추출하고 개행 문자로 연결
        return article

def flatten_list(lst : list) -> list:
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result