# from werkzeug.exceptions import HTTPException

from app_run.libs.error import APIException

"""
400:请求参数错误、401：未授权、403：禁止访问、404：没有找到资源或者页面
500：服务器产生的未知错误
200：查询成功、201：插入或者更新成功、204：删除成功
301：重定向
"""


class Success(APIException):
    code = 200
    msg = 'ok'
    error_code = 0
    data = []


class DeleteSuccess(Success):
    code = 204
    error_code = -1


class ServerError(APIException):
    code = 500
    msg = 'sorry, we made a mistake'
    error_code = 999


class ClientTypeError(APIException):
    code = 400
    msg = '请求参数错误'
    error_code = 1001


class ParameterException(APIException):
    code = 400
    msg = '请求参数异常'
    error_code = 1002


class ClientEnumError(APIException):
    code = 400
    msg = '枚举参数错误'
    error_code = 1003


class ClientRedoError(APIException):
    code = 400
    msg = '数据已经存在'
    error_code = 1004


class NotFound(APIException):
    code = 404
    msg = '没有找到'
    error_code = 1005


class AuthFailed(APIException):
    code = 401
    error_code = 1006
    msg = '密码输入错误，授权失败'


class Forbidden(APIException):
    code = 403
    error_code = 1007
    msg = '没有权限'


class FileError(APIException):
    code = 403
    error_code = 1008
    msg = '文件错误'


class TokenExceed(APIException):
    code = 401
    error_code = 1009
    msg = '身份验证信息过期'
