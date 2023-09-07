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

def find_last_page(date : int, max_page : int):
    missing_pages = []

    with ThreadPoolExecutor(max_workers=500) as executor:
        futures = [executor.submit(lambda i: check_page(date, i), i) for i in range(max_page)]

        # tqdm을 사용하여 작업 진행률 표시
        for future in tqdm(futures, total=max_page, unit="page"):
            result = future.result()
            if result is not None:
                missing_pages.append(result)

    if missing_pages:
        return min(missing_pages)  # 최솟값 반환
    else:
        return None
    
    
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
















































