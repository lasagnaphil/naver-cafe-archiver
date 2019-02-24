from bs4 import BeautifulSoup as bs

from dataclasses import dataclass
from typing import Optional, List, Tuple
import uuid
from file_downloader import FileDownloader

@dataclass
class ArticleData:
    title: str
    bulletin: str
    date: str
    author: str
    author_rank: str
    content: str
    metadata: Optional[ArticleMetaData]

class ArticleMetaData:
    images: List[uuid.UUID]
    videos: List[uuid.UUID]
    files: List[uuid.UUID]

def parse_article_ids(html_doc: str) -> Optional[List[int]]:
    soup = bs(html_doc, 'html.parser')

    # If article list does not exist anymore, abort and return None
    article_album_sub = soup.select_one('ul.article-album-sub')
    if article_album_sub:
        none_text = article_album_sub.select_one('span.m-tcol-c').get_text()
        if '없습니다' in none_text:
            return None
    
    trs = soup.select('div.article-board')[1].select_one('table.board-box').tbody.find_all('tr', attrs={"align": "center"})
    article_ids = [int(tr.select_one('span.list-count').get_text()) for tr in trs]
    return article_ids


def parse_article(dl: FileDownloader, html_doc: str, use_plain_text_content: bool = False) -> Optional[ArticleData]:
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
        metadata = None
    else:
        content_soup = soup.select_one('#tbody')
        content, metadata = parse_article_content(content_soup)

    return ArticleData(title, bulletin, date, author, author_rank, content, metadata)

def parse_article_content(dl: FileDownloader, soup) -> Tuple[str, ArticleMetaData]:
    soup = bs(html_doc, 'html.parser')

    # TODO: extract external urls from html and download it
    urls = []
    dl.download_urls(urls)
