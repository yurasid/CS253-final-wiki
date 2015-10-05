__author__ = 'yura'

from base import MainHandler
from db_models.article_model import Article
from google.appengine.api import memcache

import logging


class WikiPageHandler(MainHandler):
    def get(self, url):

        params = dict(username=None,
                      content=None,
                      url=url)

        u = self.track()
        if u:
            params['username'] = u.username


        logging.info('WPHandler: GET Start')
        logging.info('WPHandler: get content for key=%s from memcache' % url)
        content = memcache.get(url)

        if content:
            logging.info('WPHandler: content FOUND in memcache. Rendering page ... ')
            params['content'] = content
            self.render('article.jinja2', **params)
            return
        else:
            logging.info('WPHandler: No key %s in memcache, '
                         'getting article from DB' % url)
            article = Article.get_article_by_url(url)
            if article:
                logging.info('WPHandler: Article found in DB. Adding to memcache')
                params['content'] = article.content

                logging.info('WPHandler: content FOUND')
                logging.info('WPHandler: Adding key=%s to memcache' % url)
                memcache.add(url, article.content)

                logging.info('WPHandler: Rendering page ... ')
                self.render('article.jinja2', **params)

            if not article:
                logging.warning('WPHandler: No article with url= %s in DB' % url)
                logging.warning('WPHandler: redirecting to /_edit%s' % url)
                self.redirect('/_edit%s' % url)
                return


class EditPageHandler(MainHandler):

    def get(self, url):
        logging.info('EPHandler:get() => GET start')

        u = self.track()
        logging.info('EPHandler:get() => getting current user ...')

        if not u:
            logging.error('EPHandler:get() => User not log in, render error msg ...')

            self.render('article.jinja2', error_message='To create or edit the article you must '
                                                        '<a href="/login">login</a> or <a href="/signup">'
                                                        'register</a>.')
            return

        logging.info('EPHandler:get() => User is log in: %s' % u.username)
        logging.info('EPHandler:get() => Getting %s key from memcache' % url)

        content = memcache.get(url)

        if content:
            logging.info('EPHandler:get() => content FOUND')

        if not content:
            logging.warning('EPHandler:get() => Cache miss, '
                            'no article with key=%s in memcache -> DB QUERY' % url)

            a = Article.get_article_by_url(url)

            if not a:
                logging.warning('EPHandler:get() => No article with url=%s in DB. '
                                'Default content is empty string' % url)

            content = a.content if a else ''

        logging.info('EPHandler:get() => Rendering page ... ')

        self.render('edit.jinja2', content=content)
        return

    def post(self, url):

        logging.info('EPHandler:post() => POST start')
        logging.info('EPHandler:post() => Get current user ...')
        u = self.track()

        assert u is not None, 'User not log in ... END OF THE WORLD >>>> CHASSSHHHHSAHS!!!!!'

        content = self.request.get('content')

        logging.info('EPHander:post() => get content from form')

        errors = dict()
        if not content:

            logging.warning('EPHandler:post() => No content found. Rendering page with error ...')

            errors['content_error'] = 'Content cannot be empty.'
            self.render('edit.jinja2', **errors)
            return

        logging.info('EPHandler:post() => Geting article with url=%s form DB' % url)

        a = Article.get_article_by_url(url)

        if not a:

            logging.warning('EPHandler:post() => No article found. Make new article')

            a = Article.make_article(content=content, url=url, author=u.key)

            logging.info('EPHandler: Add key=%s to memcache' % url)
            memcache.add('%s' % url, content)

        else:
            logging.info('EPHandler: Article found in DB. Updating article.content')
            a.content = content

            logging.info('EPHandler: Replace key=%s in memcache' % url)
            memcache.replace('%s' % url, content)

        logging.info('EPHandler: Put article to DB')
        a.put()

        logging.info('EPHandler: Redirecting to %s url' % url)
        self.redirect(url)