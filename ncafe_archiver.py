from selenium import webdriver
from selenium.webdriver.support import ui
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

import sys
import time
import random
import getpass
import itertools
from itertools import zip_longest
import argparse
from typing import Optional, List, Iterable

from article import ArticleData, parse_article_ids, parse_article
from database import DBManager
from file_downloader import FileDownloader

def take(n, iterable):
    return list(islice(iterable, n))

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def main():
    parser = argparse.ArgumentParser(description='NAVER Cafe Archiver.')

    subparsers = parser.add_subparsers()
    download_parser = subparsers.add_parser('download')
    export_parser = subparsers.add_parser('export')

    download_parser.add_argument('cafe_name', type=str, help='NAVER Cafe name')
    download_parser.add_argument('-b', '--browser', nargs='?', type=str, choices=['chrome', 'firefox', 'ie', 'opera'], default='firefox')
    download_parser.add_argument('-l', '--auto-login', action='store_true')
    download_parser.add_argument('-p', '--use-plain-text', action='store_true')
    download_parser.set_defaults(func=download)

    export_parser.set_defaults(func=export)

    args = parser.parse_args()
    args.func(args)

def download(args):
    db = DBManager('{}.db'.format(args.cafe_name))
    db.create_tables()

    if args.browser == 'firefox':
        driver = webdriver.Firefox()
    elif args.browser == 'chrome':
        driver = webdriver.Chrome()
    elif args.browser == 'ie':
        driver = webdriver.Ie()
    elif args.browser == 'opera':
        driver = webdriver.Opera()

    if args.auto_login:
        naver_id = getpass.getpass('Naver ID: ')
        naver_pw = getpass.getpass('Naver Password: ')
        selenium_login(driver, args.cafe_name, naver_id, naver_pw)
    else:
        driver.get("https://nid.naver.com/nidlogin.login")
        input("새로 생긴 브라우저 창에서 로그인을 완료하고 Enter를 눌러주세요.")

    list_url_template = "https://cafe.naver.com/{}?iframe_url=/ArticleList.nhn%3FuserDisplay=50%26search.page={}"

    print('게시판 목록을 스캔하는 중...')
    article_ids = []
    for list_page_id in itertools.count(start=1):
        list_url = list_url_template.format(args.cafe_name, list_page_id)
        driver.get(list_url)
        driver.switch_to.frame('cafe_main')
        new_article_ids = parse_article_ids(driver.page_source)
        if new_article_ids is None:
            break
        article_ids.extend(new_article_ids)

    print('게시물을 다운로드하는 중...')
    page_url_template = 'https://cafe.naver.com/{}/{}'
    dl = FileDownloader()

    for article_id in tqdm(article_ids):
        page_url = page_url_template.format(args.cafe_name, article_id)
        driver.get(page_url)
        driver.switch_to.frame('cafe_main')
        article = parse_article(dl, driver.page_source, args.use_plain_text)
        db.insert_article(article)

    dl.shutdown()
    db.cleanup()

# Reference: https://yahwang.github.io/posts/4
# NOTE: Sadly this won't work :( Naver seems to detect these kinds of automatic logins
def selenium_login(driver, cafe_name: str, naver_id: str, naver_pw: str):
    # 네이버 메인에 최초 한 번 접근 후에 로그인 페이지로 접속하는 방법이다. (다른 분의 글에서 도움을 받았다)
    driver.get("http://www.naver.com/") 
    time.sleep(random.uniform(2,5))
    driver.find_element_by_css_selector('#account > div > a > i').click() # 로그인 페이지 접속
    time.sleep(random.uniform(3,6))

    # 아이디와 비밀번호도 키보드가 입력한 것처럼 하나하나씩 입력한다.
    for c in naver_id:
        time.sleep(random.uniform(0.15, 0.25))
        driver.find_element_by_name('id').send_keys(c)
    time.sleep(random.uniform(1,3))
    for c in naver_pw:
        time.sleep(random.uniform(0.15, 0.25))
        driver.find_element_by_name('pw').send_keys(c)
    time.sleep(random.uniform(1,3)) 
    driver.find_element_by_css_selector('#frmNIDLogin > fieldset > input').click()

def export(args):
    print('TODO...')

if __name__ == "__main__":
    main()
