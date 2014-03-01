import locale
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

import os

from flask import Flask

app = Flask(__name__,
            template_folder='../templates', 
            static_folder='../static')
import config
app.config.from_object(config)

import labevents.database

import labevents.views
