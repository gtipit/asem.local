# -*- coding: utf-8 -*-
from asem import asem
from flask import Flask, __version__, request, session, g, redirect
from flask import  url_for, abort, render_template, flash, make_response

from subprocess import check_output
from psutil import virtual_memory

import sqlite3
from datetime import datetime

DATABASE = '../onewinet/digitemp.sqlite'

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


@asem.route('/jqplot')
def jqplot():
    page_name = u'Графики'
    # s1 = [[2001,1], [2002,2],[2003,3]]
    # cur = get_db().cursor()
    query = ''' SELECT cdt_cdate, cdt_ctime, cdt_value
                FROM curdata
                WHERE cdt_cdate > '2016-01-01'
                    and cdt_prylad = 2
    '''
    cur = get_db().execute(query)
    rows = cur.fetchall()
    s1 = []
    for row in rows:
        s1.append([datetime.combine(datetime.strptime(row[0], '%Y-%m-%d'),
                                    datetime.strptime(row[1], '%H:%M:%S').time()).strftime("%Y-%m-%d %H:%M"),
                                    row[2]])
    query = ''' SELECT cdt_cdate, cdt_ctime, cdt_value
                FROM curdata
                WHERE cdt_cdate > '2016-01-01'
                    and cdt_prylad = 1
    '''
    cur = get_db().execute(query)
    rows = cur.fetchall()
    s2 = []
    for row in rows:
        s2.append([datetime.combine(datetime.strptime(row[0], '%Y-%m-%d'),
                                    datetime.strptime(row[1], '%H:%M:%S').time()).strftime("%Y-%m-%d %H:%M"),
                                    row[2]])
    cur.close()
    return render_template('jqplot.html', page_name=page_name,
        s1=s1,
        s2=s2,
        )

def get_db():
    # db = getattr(g, '_database', None)
    # if db is None:
    #     db = g._database  # = connect_to_database()
    db = sqlite3.connect(DATABASE)
    return db


@asem.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


###
## the End ##