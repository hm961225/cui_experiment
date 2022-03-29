# coding:utf-8

from flask import Flask
from config import Config
from . import models, routes

# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)  # 数据库对象
# migrate = Migrate(app, db)  # 迁移对象

def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(Config)
    models.init_db(app)
    routes.init_route(app)

    return app


# from app import routes, models  # 本app为app文件夹（包名），上面的app是实例名


'''
@app.shell_context_processor
def make_shell_context():
    """
    创建shell上下文，用于测试数据库
    """
    return {'db': db, 'User': User, 'Post': Post}
'''