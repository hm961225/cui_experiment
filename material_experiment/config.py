# coding:utf-8
import os


#  basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    SECRET_KEY = "djhqweiqda***123123dasweq"
    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:hm436464@localhost:3306/shell_test?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #SAVE_PATH = app.root_path + '/files'
    '''SQList配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    '''
