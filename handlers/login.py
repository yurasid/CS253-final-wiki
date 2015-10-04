__author__ = 'yura'

from base import MainHandler
from google.appengine.api import users
import logging
from db_models.user_model import Login


class LoginHandler(MainHandler):

    def get(self):
        u = self.track()
        if u:
            self.redirect('/')
        else:
            logging.info('LoginHandler:get() => No valid cookie, Login start ...')
            self.render('login.jinja2')

    def post(self):

        logging.info('LoginHandler:post() => Start POST')
        username = self.request.get('username')
        raw_password = self.request.get('password')

        if not (username and raw_password):
            logging.error('LoginHandler:post() => User or password blank, render form whith error msg ...')
            self.render('login.jinja2', error='Login or password fail')
            return

        logging.info('LoginHandler:post() => Login and password verify ...')
        u = Login.check_user_password(login=username, raw_password=raw_password)
        if u:
            logging.info('LoginHandler:post() => Login success, user in DB. Set cookie')
            self.set_cookie(u.make_cookie())
            self.redirect('/')
        else:
            logging.error('LoginHandler:post() => User or passwprd fail. No user in DB, or wrong password')
            self.delete_cookie()
            self.render('login.jinja2', error='Login or password fail')


class LogoutHandler(MainHandler):
    def get(self):
        self.delete_cookie()
        self.redirect('/')