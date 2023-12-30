"""
@Project ：wang_-sr_flask 
@File    ：web_test.py
@IDE     ：PyCharm 
@Auth    ：冯珂
@Time    ：2023/12/28 20:59 
@Function：
"""
from flask import render_template, request

from app_run.libs.redprint import Redprint


api = Redprint('system')


@api.route('/login')
def login():
    return render_template('login.html')


@api.route('/register')
def register():
    return render_template('register.html')
