__author__ = 'yura'

import webapp2
import jinja2
import os

# ========================
# Jinja2 Helper functions
# and BaseHandler class
# ========================

templates = os.path.join(os.path.dirname('__file__'), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates),
                               autoescape=True)

# A little handy datetime filter for jinja2
# from here: http://jinja.pocoo.org/docs/dev/api/#custom-filters


def datetimeformat(value, formating='%c'):
    #'%H:%M / %d. %b \'%y'):
    return value.strftime(formating)

jinja_env.filters['datetime'] = datetimeformat


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class BaseHandler(webapp2.RequestHandler):

    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))
        return

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        return



