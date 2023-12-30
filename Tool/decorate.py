import time
from functools import wraps
from threading import Thread

from flask import request, current_app

from Tool.Common_Func import Token
from Tool.Redis import Redis
from app.libs.enums import FileTypeEnum
from app.models.base import db
from app.libs.error_code import FileError, Forbidden, AuthFailed, NotFound, TokenExceed
from app.models.pc_user import PcUser


def print_time(f):
    """
    运行时间装饰器
    """

    def fi(*args, **kwargs):
        s = time.time()
        res = f(*args, **kwargs)
        print('--> RUN TIME: <%s> : %s' % (f.__name__, time.time() - s))
        return res

    return fi


def request_check(func):
    """
    登录检验
    """

    @wraps(func)
    def login(*args, **kwargs):
        headers_token = request.headers.get('token')
        # 判断浏览器请求头有无token
        if headers_token is None:
            return Forbidden()
        else:
            nickname = Token(key=current_app.config['SECRET_KEY']).verify_auth_token(token=headers_token).\
                data.get('nickname')
            R = Redis()
            R_token = R.get_str(mobile=nickname)
            if R_token is None:
                return TokenExceed()
            else:
                if R_token == headers_token:
                    R.set_str(mobile=nickname, codes=R_token, time=current_app.config['TOKEN_EXPIRATION'])
                else:
                    return TokenExceed(msg='token错误')
        return func(*args, **kwargs)

    return login


def file_bmp(func):
    """
    上传文件格式以及权限校验器
    """

    @wraps(func)
    def file(*args, **kwargs):
        files = request.files.get('files')
        # 获取文件后缀名
        suffix = files.filename.split('.')[-1].lower()
        file_type_list = [v.name.lower() for v in FileTypeEnum]  # 获取允许文件格式列表
        # 判断文件格式是否是可以上传的文件
        if suffix not in file_type_list:
            return FileError()
        # 判断上传者有没有上传文件的权限
        headers_token = request.headers.get('token')
        user_id = Token(key=current_app.config['SECRET_KEY']).verify_auth_token(token=headers_token).data.get('ID')
        with db.auto_commit():
            query = db.session.query(PcUser). \
                filter(PcUser.id == user_id). \
                filter(PcUser.is_delete == 0). \
                filter(PcUser.is_disable == 0).first()
            if not query:
                return NotFound()
            if query.is_IO != 1:
                return Forbidden(msg='没有上传文件的权限')
        return func(*args, **kwargs)

    return file


def asyncz(func):
    """
    异步装饰器
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs, name=func.__name__)
        thr.start()

    return wrapper


# 单例模式
def Singleton(cls):
    """
    利用装饰器实现单例模式
    """
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton
