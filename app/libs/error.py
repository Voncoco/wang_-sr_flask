from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = 'sorry, 服务器异常'
    error_code = 999
    data = []

    def __init__(self, msg=None, code=None, error_code=None, data=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        if data:
            self.data = data
        self.request = self.get_url_no_parm()
        super().__init__(msg, None)

    def get_body(self, environ=None, scope=None) -> str:
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.request,
            data=self.data
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None, scope=None):
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_parm():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
