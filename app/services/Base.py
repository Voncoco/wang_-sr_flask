import decimal
import datetime

from flask import request, current_app
from sqlalchemy.orm import Query

from Tool.Common_Func import Token
from app.libs.error_code import Forbidden


class BaseService:

    def __init__(self):
        self._user_id = None
        self._nickname = None
        self._data = None
        self._form = None
        self._files = None
        self._args = None
        self.user = {}

    @property
    def _token(self):
        token = request.headers.get('token', None)
        if token:
            return token
        else:
            raise Forbidden()

    def get_user_dic(self):
        if self._user_id or self._nickname is None:
            self._user_id = Token(key=current_app.config['SECRET_KEY']). \
                verify_auth_token(token=self._token).data.get('ID')
            self._nickname = Token(key=current_app.config['SECRET_KEY']). \
                verify_auth_token(token=self._token).data.get('nickname')
        self.user = {
            "user_id": self._user_id,
            "user_name": self._nickname
        }
        return self.user

    def get_data(self, key=None):
        if self._data is None:
            if key:
                self._data = request.get_json(silent=True).get(key)
            else:
                self._data = request.get_json(silent=True)
        return self._data

    def get_form_data(self, key=None):
        if self._form is None:
            if key:
                self._form = request.form.to_dict().get(key)
            else:
                self._form = request.form.to_dict()
        return self._form

    def get_args(self, key=None):
        if self._args is None:
            if key:
                self._args = request.args.to_dict().get(key)
            else:
                self._args = request.args.to_dict()
        return self._args

    def get_files(self, key=None):
        if self._files is None:
            if key:
                self._files = request.files.get(key)
            else:
                self._files = request.files
        return self._files

    @staticmethod
    def query_to_dict(data):
        if data is None:
            return {}

        if isinstance(data, Query):
            raise Exception("query_to_dict，数据格式Query")

        if isinstance(data, list):
            raise Exception("query_to_dict，数据格式list")

        result = {}
        if hasattr(data, "__dict__"):  # 实体结果
            for key, value in data.__dict__.items():
                if key != '_sa_instance_state':  # 实体自带属性。不能用del dict[key] 模式,否则实体会移除这个属性，查询报错
                    if isinstance(value, datetime.datetime):
                        value = value.strftime('%Y-%m-%d %H:%M:%S')
                    if isinstance(value, datetime.date):
                        value = value.strftime('%Y-%m-%d')
                    result[key] = value
        else:  # 匿名结果
            column = data.keys()
            for v in column:
                value = getattr(data, v)
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')

                if isinstance(value, datetime.date):
                    value = value.strftime('%Y-%m-%d')
                result[v] = value

        return result

    def query_to_list(self, query):
        if query is None:
            return []
        result = [self.query_to_dict(v) for v in query]
        return result
