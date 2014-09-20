import locale
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

from flask import Flask
from beaker.middleware import SessionMiddleware

app = Flask(__name__,
            template_folder='../templates', 
            static_folder='../static')

app.wsgi_app = SessionMiddleware(app.wsgi_app, {
    'session.type': 'file',
    'session.url': '127.0.0.1:11211',
    'session.data_dir': './cache',
})

import config

app.config.from_object(config)

import labevents.database

import labevents.views
