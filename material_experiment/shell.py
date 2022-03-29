# coding:utf-8
from app import app
from flask_cors import CORS
if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run(host="0.0.0.0", port=7001)
