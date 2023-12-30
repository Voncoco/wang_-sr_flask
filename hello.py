"""
@Project ：wang_-sr_flask 
@File    ：hello.py
@IDE     ：PyCharm 
@Auth    ：冯珂
@Time    ：2023/12/30 19:17 
@Function：
"""
# app.py
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'
