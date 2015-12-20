# -*- coding: utf-8 -*-
from asem import asem
from flask import Flask, __version__, request, session, g, redirect
from flask import  url_for, abort, render_template, flash, make_response

from subprocess import check_output
from psutil import virtual_memory


@asem.route('/')
@asem.route('/index')
def index():
    # return "Hello! I am ASEM. <br> Flask version - %s" % __version__
    return render_template('index.html', flask_version = __version__)
###


@asem.route('/config')
def config():
    page_name = u'Конфигурация'
    host_name = check_output('hostname')
    # Архитектура
    host_osys = 'Raspbian GNU/Linux %s' % check_output(['cat', '/etc/debian_version'])
    host_kern = check_output(['uname', '-rm'])
    host_free = virtual_memory()
    disk_stat = check_output(['df', '-h']).decode('utf-8')
    return render_template('config.html', page_name=page_name,
        host_name=host_name,
        host_osys=host_osys,
        host_kern=host_kern,
        host_free=host_free,
        disk_stat=disk_stat,
        )


###
## the End ##