import os


basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'asem.sqlite')
SQLALCHEMY_BINDS = {
    # 'digitemp': 'sqlite:///' + os.path.join(basedir, 'digitemp.sqlite'
    # 'digitemp': 'sqlite:///' + os.path.join('../../digitemp', 'digitemp.sqlite'),
    'digitemp': 'sqlite:////home/data/work/digitemp/digitemp.sqlite',
}
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
# print SQLALCHEMY_BINDS
# print SQLALCHEMY_DATABASE_URI
