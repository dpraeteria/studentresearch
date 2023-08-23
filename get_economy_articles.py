import requests
from bs4 import BeautifulSoup

def get_href(soup) :
    # 각 분야별 속보 기사에 접근할 수 있는 href를 리스트로 반환
    
    result = []
    
    div = soup.find("div", class_="list_body newsflash_body")
    
    for dt in div.find_all("dt", class_="photo"):
        result.append(dt.find("a")["href"])
        
    return result

def get_request(section) :
    # 입력된 분야에 맞는 request 객체를 반환
    # 아래 url에 쿼리를 적용한 것을 반환
    custom_header = {
        'referer' : 'https://www.naver.com/',
        'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    
    url = "https://news.naver.com/main/list.nhn"
    
    sections = {
        "정치" : 100,
        "경제" : 101,
        "사회" : 102,
        "생활" : 103,
        "세계" : 104,
        "과학" : 105
    }
    
    req = requests.get(url, headers = custom_header,
        params = {"sid1" : sections[section]}) # params 매개변수를 올바르게 설정
    return req

def get_links() :
    list_href = []
    
    # 섹션을 입력
    section = "경제"
    
    req = get_request(section)
    soup = BeautifulSoup(req.text, "html.parser")
    
    list_href = get_href(soup)
    return list_href


