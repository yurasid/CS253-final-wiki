__author__ = 'yura'
from base import MainHandler
from lib.validate import validation_form
from db_models.user_model import Login

import logging


class SignupHandler(MainHandler):
    def get(self):
        self.render('signup.jinja2')

    def post(self):

        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        errors_form = validation_form(username=username,
                                      password=password,
                                      verify=verify,
                                      email=email)

        if errors_form:
            logging.error('SignupHandler: Error by parsing form. Render form with error msg ...')
            self.render('signup.jinja2', **errors_form)
            return

        logging.info('SignupHandler: Check if user registred. Making DB QUERY')
        u = Login.get_by_username(username)

        logging.warning('SignupHandler: from DB by username %s get => %s' % (username, u))

        if u:
            logging.error('SignupHandler: User registred. Set error message')
            self.render('signup.jinja2', error_username='Login exist')
            return

        logging.info('SignupHandler: Make a user')
        u = Login.create_user(username=username,
                              raw_password=password,
                              email=email)

        logging.info('SignupHandler: Put user to DB')
        u.put()

        logging.info('SignupHandler: Make token and set cookie for current user')
        self.set_cookie(u.make_cookie())

        self.redirect('/')



