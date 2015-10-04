__author__ = 'yura'

from google.appengine.ext import ndb
import json


class Article(ndb.Model):
    content = ndb.TextProperty(required=True)
    url = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    author = ndb.KeyProperty()
    modify_time = ndb.DateTimeProperty(auto_now=True)
    modify_username = ndb.KeyProperty()

    @classmethod
    def make_article(cls, content=content, url=url,
                     author=None, modify_username=None):
        """
        Make an article instance

        :param content: <str>
            Article raw text
        :param url: <str>
            Url of an article
        :param author: <ndb.Key>
            Key object of author
        :param modify_username: <ndb.Key>
            Key object of last user that modify the article
        :return: <Article>
            Article instance or None
        """
        if not (content and url):
            return None
        a = Article()
        a.populate(content=content, author=author,
                   modify_username=modify_username, url=url)
        return a

    @classmethod
    def get_article_by_url(cls, url):
        """
        Get article by url

        :param url: <str>
            url of the article
        :return: <Article>
            Article instance
        """
        a = cls.query(cls.url == url)
        return a.get()

    def get_json(self):
        """
        Make a json object for Article

        :return:
            json string
        """
        d = dict()
        d['url'] = self.url
        d['content'] = self.content
        d['created'] = self.created.strftime('%c')
        return json.dumps(d)
