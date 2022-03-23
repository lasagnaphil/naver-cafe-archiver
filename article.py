from dataclasses import dataclass
from bs4 import BeautifulSoup as bs
from typing import Optional
import re

@dataclass
class ArticleData:
    title: str
    bulletin: str
    date: str
    author: str
    author_rank: str
    content: str

link_board_regex = re.compile(r"search\.clubid=([0-9]+)")
count_regex = re.compile(r"조회 ([0-9]+)")

def parse_article(html_doc: str, use_plain_text_content: bool = False) -> Optional[ArticleData]:
    soup = bs(html_doc, 'html.parser')

    content_box = soup.select_one('div.ArticleContentBox')

    div_article_title = content_box.select_one('div.ArticleTitle')
    a_link_board = div_article_title.select_one('a.link_board')
    board_id = int(re.search(link_board_regex, a_link_board.get('href'))[1])
    board = a_link_board.text
    title = div_article_title.select_one('h3.title_text').text

    div_writer_info = content_box.select_one('div.WriterInfo')
    writer_name = div_writer_info.select_one('button.nickname').text
    writer_rank = div_writer_info.select_one('em.nick_level').text

    div_article_info = content_box.select_one('div.article_info')
    date = div_article_info.select_one('span.date').text
    count = int(re.match(count_regex, div_article_info.select_one('span.count').text)[1])

    div_se_viewer = content_box.select_one('div.se-viewer')
    contents = div_se_viewer.get_text()

    return ArticleData(title, board, date, writer_name, writer_rank, contents)


