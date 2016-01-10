# -*- coding: utf-8 -*-
from asem import asem
from flask import Flask, __version__, request, session, g, redirect
from flask import url_for, abort, render_template, flash, make_response

from subprocess import check_output
from psutil import virtual_memory

import sqlite3
from datetime import datetime
from datetime import timedelta

DATABASE = '../onewinet/digitemp.sqlite'


@asem.route('/')
@asem.route('/index')
def index():
    # return "Hello! I am ASEM. <br> Flask version - %s" % __version__
    return render_template('index.html', flask_version=__version__)
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
    '''Первая версия, последние три дня...'''
    sdate = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    page_name = u'Графики'
    avias = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    seres = [[] for i in avias]
    # cur = get_db().cursor()
    query = ''' SELECT cdt_prylad, cdt_cdate, cdt_ctime, cdt_value
                FROM curdata
                WHERE cdt_cdate > '%s'
                    and cdt_prylad in (%s)
    ''' % (sdate, ', '.join([str(x) for x in avias]))
    # print query
    cur = get_db().execute(query)
    rows = cur.fetchall()
    # s1 = []
    for row in rows:
        seres[row[0]].append([datetime.combine(datetime.strptime(row[1], '%Y-%m-%d'),
                                               datetime.strptime(row[2], '%H:%M:%S').time()
                                               ).strftime("%Y-%m-%d %H:%M"),
                             row[3]])
    cur.close()
    # print seres
    return render_template('jqplot.html', page_name=page_name,
                           seres=seres,
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
# # the End # #
