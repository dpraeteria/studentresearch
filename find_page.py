import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36"}

url_parsing = lambda date, page:f"https://news.daum.net/breakingnews/economic?regDate={date}&page={page}"

def check_page(date, i):
    req = requests.get(url_parsing(date, i+1), headers=header)
    if req.text == requests.get(url_parsing(date, i), headers=header).text and i != 0:
        return i
    return None

def find_last_page(date, max_page):
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
