# -*- coding: utf-8 -*-
from asem import asem
from flask import Flask, __version__, request, session, g, redirect
from flask import  url_for, abort, render_template, flash, make_response


@asem.route('/')
@asem.route('/index')
def index():
    return "Hello, Asem! <br> Flask version - %s" % __version__
###


@asem.route('/config')
def config():
    pageName = u'Конфигурация'
    return render_template('config.html', pageName=pageName)
###
## the End ##