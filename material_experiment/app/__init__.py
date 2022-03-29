# coding:utf-8

from flask import Flask, Blueprint
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)  # 数据库对象
migrate = Migrate(app, db)  # 迁移对象


from app import routes, models # 本app为app文件夹（包名），上面的app是实例名
from app.routess import *

'''
@app.shell_context_processor
def make_shell_context():
    """
    创建shell上下文，用于测试数据库
    """
    return {'db': db, 'User': User, 'Post': Post}
'''