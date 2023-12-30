from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from datetime import date

from app_run.libs.error_code import ServerError


class JSONEncode(_JSONEncoder):
    """模型序列化"""

    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        raise ServerError()


class Flask(_Flask):
    json_encoder = JSONEncode
