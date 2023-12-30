# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/3 10:54
@Auth ： 冯珂
@File ：__init__.py.py
@IDE ：PyCharm
@Motto: 
"""
from flask import Blueprint

from app.api.test import TestApi


def create_blueprint_test():
    """实例化蓝图"""
    bp_t = Blueprint('t', __name__)
    TestApi.api.register(bp_t)
    return bp_t
