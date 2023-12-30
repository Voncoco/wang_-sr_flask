from flask import jsonify, request, render_template

from Tool.decorate import request_check
from app.libs.redprint import Redprint
from app.services.User.UserService import UserService
from app.validators.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserResetPwd

api = Redprint('user')


@api.route('/test', methods=['GET'])
@request_check
def user():
    cook = request.cookies
    return jsonify(cook)


@api.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录
    """
    rm = UserService()
    data_inform = rm.login().data
    return render_template('home_page.html', data=data_inform)


@api.route('/register', methods=['GET', 'POST'])
def register():
    """
    注册
    """
    rm = UserService()
    rm.register()
    return render_template('login.html')


@api.route('/update', methods=['PUT'])
@request_check
def update():
    """
    用户修改用户信息
    """
    rm = UserService()
    return rm.update()


@api.route('/reset_pwd', methods=['PUT'])
@request_check
def reset_pwd():
    """
    修改密码
    """
    rm = UserService()
    return rm.reset_pwd()
