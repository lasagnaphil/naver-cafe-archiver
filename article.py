from dataclasses import dataclass
from bs4 import BeautifulSoup as bs
from typing import Optional

@dataclass
class ArticleData:
    title: str
    bulletin: str
    date: str
    author: str
    author_rank: str
    content: str

def parse_article(html_doc: str, use_plain_text_content: bool = False) -> Optional[ArticleData]:
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

    return ArticleData(title, bulletin, date, author, author_rank, content)


