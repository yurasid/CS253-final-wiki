__author__ = 'yura'

from google.appengine.ext import ndb
from webapp2_extras import security
from lib.cookie import make_token_cookie
import logging


PEPPER = '28542283eb566945894f56eb22411fb291b1f845$sha1$saEPmYNMPcTAyevIivSQiD'


class Login(ndb.Model):
    username = ndb.StringProperty(required=True)
    pw_hash = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create_user(cls, username=None, raw_password=None, email=None):
        logging.info('LoginClass:create_user() => Start creating user')

        if not(username and raw_password):
            logging.error('LoginClass:create_user() => username or raw_password is empty, return None')
            return None

        salt = security.generate_random_string(length=30)
        logging.info('LoginClass:create_user() => Making salt for password hash ... < %s >' % salt)

        pw_hash = security.generate_password_hash(raw_password, pepper=PEPPER)
        logging.info('LoginClass:create_user() => Generatin password hash ... < %s >' % pw_hash)
        u = Login()
        u.populate(username=username,
                   pw_hash=pw_hash,
                   email=email)
        logging.info('LoginClass:create_user() => Make and return Login instance')
        return u

    @classmethod
    def check_user_password(cls, login=None, raw_password=None):
        """
        :param login:
            login
        :param raw_password:
            password
       :return:
            Login instance or None
        """
        logging.info('LoginClass:check_user_password() => Strat check_user_password()')
        if not raw_password:
            logging.info('LoginClass:check_user_password() => raw_password is empty, return None')
            return None
        logging.info('LoginClass:check_user_password() => Making QUERY to DB to get user instance')
        u = cls.query(Login.username == login).get()
        if not u:
            logging.error('LoginClass:check_user_password() => User NOT found. Return None')
            return None
        logging.info('LoginClass:check_user_password() => User FOUND')

        # comment for production
        # return u if security.check_password_hash(raw_password, u.pw_hash, pepper=PEPPER) else None

        sec_check = security.check_password_hash(raw_password, u.pw_hash, pepper=PEPPER)
        logging.info('LoginClass:check_user_password() => Result of security.check_password_hash() is %s' % sec_check)
        logging.info('LoginClass:check_user_password() => Return user instance or if True and None otherwise')
        return u if sec_check else None

    @classmethod
    def _query_by_username(cls, username):
        u_query = cls.query(Login.username == username)
        return u_query

    @classmethod
    def get_by_username(cls, username):
        q = cls._query_by_username(username)
        return q.get() if q else None

    def make_cookie(self):
        return make_token_cookie(self.key.id())
