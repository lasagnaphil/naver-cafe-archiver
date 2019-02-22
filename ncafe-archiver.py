from selenium import webdriver
from selenium.webdriver.support import ui
from bs4 import BeautifulSoup as bs
import pandas as pd

from dataclasses import dataclass

import sys
import time
import random
import getpass

def main():
    club_name = sys.argv[1]
    club_max_article_id = sys.argv[2]
    # naver_id = getpass.getpass('Naver ID: ')
    # naver_pw = getpass.getpass('Naver Password: ')

    driver = webdriver.Firefox()
    driver.get("http://www.naver.com/") 

    # Login manually within 10 seconds!
    time.sleep(10)

    # selenium_login(driver, club_name, club_max_article_id, naver_id, naver_pw)

    driver.get('https://cafe.naver.com/snugdc/6274')
    driver.switch_to.frame('cafe_main')
    article = parse_article(driver.page_source)
    print(article)

'''
    url_template = 'https://cafe.naver.com/{}/{}'
    for article_id in range(1, club_max_article_id + 1):
        page_url = url_template.format(club_name, article_id)
        driver.get(page_url)
        driver.switch_to.frame('cafe_main')
        parse_article(driver.page_source)
'''

def selenium_login(driver, club_name: str, club_max_article_id: int, naver_id: str, naver_pw: str):
    # 네이버 메인에 최초 한 번 접근 후에 로그인 페이지로 접속하는 방법이다. (다른 분의 글에서 도움을 받았다)
    driver.get("http://www.naver.com/") 
    time.sleep(random.randrange(2,5))
    driver.find_element_by_css_selector('#account > div > a > i').click() # 로그인 페이지 접속
    time.sleep(random.randrange(3,6))

    # 아이디와 비밀번호도 키보드가 입력한 것처럼 하나하나씩 입력한다.
    for c in naver_id:
        time.sleep(0.02)
        driver.find_element_by_name('id').send_keys(c)
    time.sleep(random.randrange(1,3))
    for c in naver_pw:
        time.sleep(0.02)
        driver.find_element_by_name('pw').send_keys(c)
    time.sleep(random.randrange(1,3)) 
    driver.find_element_by_css_selector('#frmNIDLogin > fieldset > input').click()

@dataclass
class Article:
    title: str
    bulletin: str
    date: str
    author: str
    content: str

def parse_article(html_doc: str) -> Article:
    soup = bs(html_doc, 'html.parser')

    title_box = soup.select_one('div.tit-box')

    title = title_box.select_one('span.b').get_text()
    bulletin = title_box.select_one('td.m-tcol-c a.m-tcol-c').get_text()
    date = title_box.select_one('div.fr td.date').get_text()

    etc_box = soup.select_one('div.etc-box')

    author = etc_box.select_one('td.nick td.pc2w').a.get_text()

    content_tags = soup.select_one('#tbody').select('p')
    content = '\n'.join([tags.get_text() for tags in content_tags])

    return Article(title, bulletin, date, author, content)

if __name__ == "__main__":
    main()
