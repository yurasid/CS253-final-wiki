__author__ = 'yura'

from google.appengine.ext import ndb
from webapp2_extras import security
from lib.cookie import make_token_cookie


class Login(ndb.Model):
    username = ndb.StringProperty(required=True)
    pw_hash = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create_user(cls, username=None, raw_password=None, email=None):
        if not(username and raw_password):
            return None
        salt = security.generate_random_string(length=30)
        pw_hash = security.generate_password_hash(raw_password, pepper=salt)
        u = Login()
        u.populate(username=username,
                   pw_hash=pw_hash,
                   email=email)
        return u

    @classmethod
    def check_user_password(cls, login=None, raw_password=None, email=None):
        """
        :param login:
            login
        :param raw_password:
            password
        :param email:
            email
        :return:
            True or False
        """
        if not raw_password:
            return False
        u = cls.query(Login.username == login).get() if login else cls.query(Login.email == email).get()
        if not u:
            return None
        return u if security.check_password_hash(raw_password, u.pw_hash) else None

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
