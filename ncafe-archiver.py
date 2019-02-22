from selenium import webdriver
from selenium.webdriver.support import ui
from bs4 import BeautifulSoup as bs
import pandas as pd
from dataclasses import dataclass
from typing import Optional, List

import sys
import time
import random
import getpass
import itertools

def main():
    club_name = sys.argv[1]
    # naver_id = getpass.getpass('Naver ID: ')
    # naver_pw = getpass.getpass('Naver Password: ')

    driver = webdriver.Firefox()
    driver.get("http://www.naver.com/") 

    # Login manually within 10 seconds!
    time.sleep(10)

    # selenium_login(driver, club_name, club_max_article_id, naver_id, naver_pw)

    list_url_template = "https://cafe.naver.com/snugdc?iframe_url=/ArticleList.nhn%3FuserDisplay=50%26search.page={}"

    print('게시판 목록을 스캔하는 중...')
    article_ids = []
    for list_page_id in itertools.count(start=1):
        list_url = list_url_template.format(list_page_id)
        driver.get(list_url)
        driver.switch_to.frame('cafe_main')
        new_article_ids = parse_article_ids(driver.page_source)
        if new_article_ids is None:
            break
        print(new_article_ids)
        article_ids.extend(new_article_ids)

    print('게시물을 다운로드하는 중...')
    articles = []
    page_url_template = 'https://cafe.naver.com/{}/{}'
    for article_id in article_ids:
        page_url = page_url_template.format(club_name, article_id)
        driver.get(page_url)
        driver.switch_to.frame('cafe_main')
        article = parse_article(driver.page_source, use_plain_text_content=True)
        articles.append(article)
        print(article)

# Reference: https://yahwang.github.io/posts/4
# NOTE: Sadly this won't work :(
# Naver seems to detect these kinds of automatic logins
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

def parse_article_ids(html_doc: str) -> Optional[List[int]]:
    soup = bs(html_doc, 'html.parser')

    # If article list does not exist anymore, abort and return None
    article_album_sub = soup.select_one('ul.article-album-sub')
    if article_album_sub:
        none_text = article_album_sub.select_one('span.m-tcol-c').get_text()
        if '없습니다' in none_text:
            return None
    
    trs = soup.select('div.article-board')[1].select_one('table.board-box').tbody.find_all('tr', attrs={"align": "center"})
    print(trs)
    article_ids = [int(tr.select_one('span.list-count').get_text()) for tr in trs]
    return article_ids

@dataclass
class Article:
    title: str
    bulletin: str
    date: str
    author: str
    author_rank: str
    content: str

def parse_article(html_doc: str, use_plain_text_content: bool = False) -> Optional[Article]:
    soup = bs(html_doc, 'html.parser')

    title_box = soup.select_one('div.tit-box')

    title = title_box.select_one('span.b').get_text()
    bulletin = title_box.select_one('td.m-tcol-c a.m-tcol-c').get_text()
    date = title_box.select_one('div.fr td.date').get_text()

    etc_box = soup.select_one('div.etc-box')

    author = etc_box.select_one('td.nick td.p-nick').a.get_text()
    author_rank = etc_box.select_one('td.step').span.get_text()

    if use_plain_text_content:
        content_tags = soup.select_one('#tbody').select('p')
        content = '\n'.join([tags.get_text() for tags in content_tags])
    else:
        content = str(soup.select_one('#tbody'))

    return Article(title, bulletin, date, author, author_rank, content)

if __name__ == "__main__":
    main()
