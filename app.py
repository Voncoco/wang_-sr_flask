# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/13 10:08
@Auth ： 冯珂
@File ：app.py
@IDE ：PyCharm
@Motto: 
"""
from flask import render_template

from app_run import create_app
from app_run.libs.error import APIException
from werkzeug.exceptions import HTTPException
from app_run.libs.error_code import ServerError

app = create_app()


@app.errorhandler(Exception)
def framework_error(e):
    """
    全局异常处理
    """
    if isinstance(e, APIException):
        code = e.code
        msg = e.msg
        error_code = 1007
        error = APIException(msg, code, error_code)
        return render_template('error.html', code=code, msg=msg, error_code=error_code, request=error.request)
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        error = APIException(msg, code, error_code)
        return render_template('error.html', code=code, msg=msg, error_code=error_code, request=error.request)
    else:
        if not app.config['DEBUG']:
            error = ServerError()
            return render_template('error.html', code=error.code, msg=error.msg, error_code=error.error_code,
                                   request=error.request)
        else:
            raise e
