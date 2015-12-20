# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

asem = Flask(__name__)
asem.config.from_object('config')
db = SQLAlchemy(asem)

from views import views
asem.debug = True
