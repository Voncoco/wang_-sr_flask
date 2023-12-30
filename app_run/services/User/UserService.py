import json

from flask import current_app, request
from Tool.Common_Func import Salt, Token
from app_run.libs.enums import IsDeleteEnum, IsIoEnum
from app_run.libs.error_code import ClientRedoError, Success, NotFound, AuthFailed
from app_run.models.base import db
from app_run.models.pc_user import PcUser
from app_run.services.Base import BaseService


class UserService(BaseService):
    def __init__(self):
        super().__init__()
        self.user['nickname'] = self.get_form_data().get('nickname')

    def login(self):
        """
        登录
        """
        password = self.get_form_data().get('password')
        with db.auto_commit():
            # 查看有无该用户名
            nickname_query = db.session.query(PcUser).\
                filter(PcUser.nickname == self.user.get('nickname')).\
                filter(PcUser.is_disable == 0).\
                filter(PcUser.is_delete == 0).first()
            if nickname_query is None:
                response = NotFound().get_response()
                response.delete_cookie(key='token')
                raise NotFound()
            # 校验密码
            stochastic = nickname_query.stochastic
            sea_password = nickname_query.password
            data = Salt().decode(stochastic=stochastic, encrypted=sea_password)
            if data is None:
                return AuthFailed(msg="解密错误")
            elif data.get('password') != password:
                response = AuthFailed().get_response()
                response.delete_cookie(key='token')
                raise AuthFailed()
            else:
                # 生成token
                token = Token(current_app.config['SECRET_KEY']).\
                    generate_token(userid=nickname_query.id, nickname=self.user.get('nickname'),
                                   time=current_app.config['TOKEN_EXPIRATION'])
                user_info = {
                    'id': nickname_query.id,
                    'nickname': self.user.get('nickname'),
                    'phone': nickname_query.phone,
                    'email': nickname_query.Email,
                    'gender': '男' if nickname_query.gender else '女',
                    'logo_id': nickname_query.logo,
                }
                data = {'user_info': user_info,
                        'token': token}
                response = Success(data=data).get_response()
                response.set_cookie('token', token)
                return Success(data=data)

    def register(self):
        """
        注册
        """
        data = self.get_form_data()
        phone = data.get('phone')
        password = data.get('password')
        email = data.get('email')
        gender = data.get('gender')
        with db.auto_commit():
            # 校验用户名有无重复
            nickname_query = db.session.query(PcUser.nickname).\
                filter(PcUser.nickname == self.user.get('nickname')).\
                filter(PcUser.is_disable == 0).first()
            if nickname_query:
                raise ClientRedoError(msg="用户名已存在")
            # 获取随机字符串
            salt = Salt(random_length=20)
            stochastic = salt.stochastic
            # 密码加密
            encrypted_str = salt.encrypt(password=password)
            # 写入数据库
            user = PcUser()
            user.nickname = self.user.get('nickname')
            user.stochastic = stochastic
            user.is_disable = 0
            user.phone = phone
            user.password = encrypted_str
            user.Email = email
            user.gender = gender
            user.is_delete = IsDeleteEnum.未删除.value
            user.is_IO = IsIoEnum.可上传.value
            user.logo = 4 if gender == 1 else 5
            db.session.add(user)
            return Success(msg='注册成功,请登录！')

    def update(self):
        """
        修改
        """
        data = self.get_form_data()
        userid = data.get('userid')
        phone = data.get('phone')
        email = data.get('email')
        gender = data.get('gender')
        incidental = data.get('incidental')
        logo = data.get('logo')
        with db.auto_commit():
            # 查看有无该用户
            user_query = db.session.query(PcUser).\
                filter(PcUser.id == userid).\
                first()
            if user_query is None:
                raise NotFound(msg='没有该用户')
            # 校验昵称是否冲突
            user_query = db.session.query(PcUser).\
                filter(PcUser.nickname == self.user.get('nickname')).\
                filter(PcUser.id != userid).\
                filter(PcUser.is_disable == 0).first()
            if user_query:
                raise ClientRedoError(msg="用户名已存在")
            # 修改信息
            db.session.query(PcUser).\
                filter(PcUser.id == userid).\
                update({PcUser.nickname: self.user.get('nickname'),
                        PcUser.phone: phone,
                        PcUser.Email: email,
                        PcUser.gender: gender,
                        PcUser.logo: logo,
                        PcUser.incidental: json.dumps(incidental, ensure_ascii=False)})
            # 生成token
            token = Token(current_app.config['SECRET_KEY']).generate_token(userid=userid,
                                                                           nickname=self.user.get('nickname'),
                                                                           time=current_app.config['TOKEN_EXPIRATION'])
            data = {'id': userid,
                    'nickname': self.user.get('nickname'),
                    'phone': phone,
                    'Email': email,
                    'gender': '男' if gender else '女',
                    'token': token}
            response = Success(data=data).get_response()
            response.set_cookie('token', token)
            return response

    def reset_pwd(self):
        """
        修改密码
        """
        new_password = self.get_form_data().get('new_password')
        with db.auto_commit():
            headers_token = request.headers.get('token')
            user_data = Token(key=current_app.config['SECRET_KEY']).verify_auth_token(token=headers_token).data
            self.user['nickname'] = user_data.get('nickname')
            # 获取随机字符串
            salt = Salt(random_length=20)
            stochastic = salt.stochastic
            # 密码加密
            encrypted_str = salt.encrypt(password=new_password)
            db.session.query(PcUser).\
                filter(PcUser.id == user_data.get('ID')).\
                update({PcUser.stochastic: stochastic,
                        PcUser.password: encrypted_str})

            # 生成token
            token = Token(current_app.config['SECRET_KEY']).generate_token(userid=user_data.get('ID'),
                                                                           nickname=self.user.get('nickname'),
                                                                           time=current_app.config['TOKEN_EXPIRATION'])

            response = Success().get_response()
            response.set_cookie('token', token)
            return response
