# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import time
import re

headers = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}


def create_soup(url):
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup


############### 날씨 ###############
def scrap_weather():
    weather_url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8"
    soup = create_soup(weather_url)

    weather_data = soup.find("div", attrs={"class": "info_data"})

    # 현재 날씨 정보
    weather_info = weather_data.find("p", attrs={
        "class": "cast_txt"
    }).get_text()

    # 온도
    pos_degree = weather_data.find("p", attrs={
        "class": "info_temperature"
    }).get_text().replace("도씨", "")
    min_degree = weather_data.find("span", attrs={"class": "min"}).get_text()
    max_degree = weather_data.find("span", attrs={"class": "max"}).get_text()

    # 강수 확률
    rainy_data = soup.find("li", attrs={
        "class": "date_info today"
    }).find_all("span", attrs={"class": "num"})

    # 미세먼지 정보
    dust_data = soup.find("dl", attrs={
        "class": "indicator"
    }).find_all("dd", attrs={"class": "lv2"})

    # 출력
    print("[오늘의 날씨]")
    print(f"현재 {pos_degree} (최저 {min_degree}/ 최고 {max_degree})")
    print(weather_info)
    print(
        f"오전 강수확률 {rainy_data[0].get_text()}% / 오후 강수확률 {rainy_data[1].get_text()}%"
    )
    print()
    print(f"미세먼지 {dust_data[0].get_text()}")
    print(f"초미세먼지 {dust_data[1].get_text()}")
    print()


############### News ###############
def scrap_news(sector):
    news_url = "https://news.naver.com/"
    soup = create_soup(news_url)

    # 뉴스 데이터
    news_data = soup.find("div", attrs={"id": f"section_{sector}"})
    # 섹터 이름
    sector_name = news_data.find("h4", attrs={"class": "tit_sec"}).a.get_text()
    # 헤드라인 목록
    news_list = news_data.find("ul", attrs={
        "class": "mlist2 no_bg"
    }).find_all("li")

    # 출력
    print(f"[국내 {sector_name} 헤드라인 뉴스]")
    for idx, article in enumerate(news_list):
        headline = article.a.get_text().strip()
        news_link = article.a["href"]
        print(f"{idx+1}. {headline}")
        print(f"   (링크 : {news_link} )")

    print()


############### 회화 ###############
def scrap_english():
    eng_url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english"
    soup = create_soup(eng_url)

    sentences = soup.find_all("div", attrs={"id": re.compile("^conv_kor_t")})
    print("[오늘의 영어 회화]")
    print("(영어지문)")

    # 8문장이 있다고 가정, 5~8까지 영어문장 (idx: 4~7)
    for txt in sentences[len(sentences) // 2:]:
        print(txt.get_text().strip())

    print()
    print("(한글지문)")
    # 8문장이 있다고 가정, 0~3까지 한글문장 (idx: 0~3)
    for txt in sentences[:len(sentences) // 2:]:
        print(txt.get_text().strip())
    print()


if __name__ == "__main__":
    # 오늘의 날씨 정보 가져오기
    scrap_weather()

    #### 분야별 뉴스 가져오기
    # politics : 정치
    # economy : 경제
    # it : IT/과학
    # society : 사회
    # life : 생활/문화
    # world : 세계
    scrap_news("politics")
    scrap_news("economy")
    scrap_news("it")

    # 영어 회화
    scrap_english()