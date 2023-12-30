"""
@Project ：wang_-sr_flask 
@File    ：__init__.py.py
@IDE     ：PyCharm 
@Auth    ：冯珂
@Time    ：2023/12/28 20:58 
@Function：
"""
from flask import Blueprint

from app.api.web import web_home


def create_blueprint_web():
    """实例化蓝图"""
    bp_v2 = Blueprint('web', __name__)
    web_home.api.register(bp_v2)
    return bp_v2
