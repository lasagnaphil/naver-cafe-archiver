from article import ArticleData
from peewee import *

from typing import List, Iterable

db = Proxy()

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField(unique=True)
    rank = CharField()

class Bulletin(BaseModel):
    name = CharField(unique=True)

class Article(BaseModel):
    title = CharField()
    bulletin = ForeignKeyField(Bulletin, backref='articles')
    date = DateField()
    author = ForeignKeyField(User, backref='articles')
    content = CharField()

class DBManager:
    def __init__(self, db_name: str):
        global db
        sqlite = SqliteDatabase(db_name)
        db.initialize(sqlite)
        db.connect()
        self.authors_cache = {}
        self.bulletins_cache = {}

    def create_tables(self):
        global db
        db.create_tables([User, Bulletin, Article])

    def atomic():
        global db
        return db.atomic()

    def insert_article(self, article: ArticleData):
        if article.author in self.authors_cache:
            author_id = self.authors_cache[article.author]
        else:
            author_id = User.insert({'name': article.author, 'rank': article.author_rank}).execute()
            self.authors_cache[article.author] = author_id
        if article.bulletin in self.bulletins_cache:
            bulletin_id = self.bulletins_cache[article.bulletin]
        else:
            bulletin_id = Bulletin.insert({'name': article.bulletin}).execute()
            self.bulletins_cache[article.bulletin] = bulletin_id

        Article.insert({
            'title': article.title, 
            'bulletin': bulletin_id, 
            'date': article.date, 
            'author': author_id, 
            'content': article.content
        }).execute()
        print("Inserted article: {}".format(article.title))

    def cleanup(self):
        db.close()
        self.authors_cache = None
        self.bulletins_cache = None

