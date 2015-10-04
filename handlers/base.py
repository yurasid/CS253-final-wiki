__author__ = 'yura'

from jinja2_tools import BaseHandler
from lib.cookie import verify_token
import logging
from db_models.user_model import Login


class MainHandler(BaseHandler):
    def set_cookie(self, token):
        logging.info('MainHandler:set_cookie() : set cookie header %s' % token)
        self.response.headers.add_header('Set-Cookie',
                                         'user_id=%s;Path=/' % token)

    def check_cookie(self):
        cookie = self.request.cookies.get('user_id')
        logging.info('MainHandler:check-cookie() : Checking cookie ...')
        logging.info('MainHandler:check-cookie() : And return user id if exist, None otherwise')
        return verify_token(cookie) if cookie else None

    def track(self):
        logging.info('MainHandler:track() => Geting user_id ...')
        u_id = self.check_cookie()
        logging.info('MainHandler:track() => user_id = %s' % u_id)
        if u_id:
            logging.info('MainHandler:track() => Geting Login object from DB ...')
            logging.info('MainHandler:track() => Login instanse: %s' % Login.get_by_id(int(u_id)))
            return Login.get_by_id(int(u_id))
        else:
            self.delete_cookie()
            logging.info('MainHandler:track() => No valid cookie, return None')
            return None

    def delete_cookie(self):
        logging.info('MainHandler:delete_cookie() => Delete cookie if exist')
        self.response.delete_cookie('user_id')







