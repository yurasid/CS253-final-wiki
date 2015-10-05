__author__ = 'yura'

from base import MainHandler
from google.appengine.api import users
import logging
from db_models.user_model import Login


class LoginHandler(MainHandler):

    def get(self):

        logging.info('LoginHandler:get() => Start GET')

        u = self.track()

        logging.info('LoginHandler:get() => Call track() method and getting user instance')

        if u:

            logging.info('LoginHandler:get() => Valid cookie found. User that log in is ... ' % u.username)
            logging.info('LoginHandler:get() => Redirecting to "/"(main page)')

            self.redirect('/')
        else:

            logging.info('LoginHandler:get() => No valid cookie, Login start ...')

            self.render('login.jinja2')

    def post(self):

        logging.info('LoginHandler:post() => Start POST')
        username = self.request.get('username')
        raw_password = self.request.get('password')

        if not (username and raw_password):

            logging.error('LoginHandler:post() => User or password blank, render form with error msg ...')

            self.render('login.jinja2', error='Login or password fail')
            return

        logging.info('LoginHandler:post() => Login and password verify ...')
        logging.info('LoginHandler:post() => Call Login.check_user_password() method ...')

        u = Login.check_user_password(login=username, raw_password=raw_password)
        if u:

            logging.info('LoginHandler:post() => Login success, user in DB. Set cookie')

            self.set_cookie(u.make_cookie())

            logging.error('LoginHandler:post() => Redirecting to main page')

            self.redirect('/')
        else:

            logging.error('LoginHandler:post() => User or passwprd fail. No user in DB, or wrong password')

            self.delete_cookie()

            logging.error('LoginHandler:post() => User or password FAIL, render form with error msg ...')
            self.render('login.jinja2', error='Login or password fail')


class LogoutHandler(MainHandler):
    def get(self):
        logging.error('LogoutHandler:get() => Start GET')
        self.delete_cookie()

        logging.error('LogoutHandler:get() => Redirecting to main page')
        self.redirect('/')