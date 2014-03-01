import locale
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

from flask import Flask

from flask.ext.login import LoginManager

app = Flask(__name__,
            template_folder='../templates', 
            static_folder='../static')
import config
app.config.from_object(config)

login_manager = LoginManager(app)


import labevents.database

import labevents.views
