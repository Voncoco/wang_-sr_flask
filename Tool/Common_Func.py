
from itsdangerous import JSONWebSignatureSerializer, BadSignature, TimedJSONWebSignatureSerializer as Serializer, \
    SignatureExpired
import random

from Tool.Redis import Redis
from app.libs.error_code import Success, AuthFailed, TokenExceed


class Salt:
    """
    数据加密
    """
    def __init__(self, random_length=20):
        self.random_length = random_length
        self.stochastic = self.random_str()

    def random_str(self):
        """
        生成一个指定长度的随机字符串
        """
        stochastic = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
        length = len(base_str) - 1
        for i in range(self.random_length):
            stochastic += base_str[random.randint(0, length)]
        return stochastic

    def encrypt(self, password):
        """
        将密码加密
        """
        s = JSONWebSignatureSerializer(self.stochastic)
        encrypted = s.dumps({'password': password}).decode()
        return encrypted

    @staticmethod
    def decode(stochastic, encrypted):
        """
        stochastic:随机字符串
        Encrypted：加密字符串
        解密结果
        """
        s = JSONWebSignatureSerializer(stochastic)
        try:
            data = s.loads(encrypted)
            return data
        except BadSignature:
            return None


class Token:
    """
    token生成以及解析
    """
    def __init__(self, key):
        self.key = key

    def generate_token(self, userid, nickname, time):
        """
        生成token，写入Redis
        """
        s = Serializer(self.key)
        token = s.dumps({'ID': userid, 'nickname': nickname}).decode()
        R = Redis()
        R.set_str(mobile=nickname, codes=token, time=time)
        return token

    def verify_auth_token(self, token):
        """
        解析token
        """
        s = Serializer(self.key)
        try:
            data = s.loads(token)
            return Success(data=data)
        except SignatureExpired:
            # token过期
            raise TokenExceed()
        except BadSignature:
            # token错误
            raise TokenExceed(msg='token错误')


if __name__ == '__main__':
    a = Token('6u1qo2qlp-1vs3zr2rm+%971hv^s=tb2m0_y2^3bkjllsdib!8')
    token = a.verify_auth_token(
        'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY2OTk2Mzg0NCwiZXhwIjoxNjY5OTY3NDQ0fQ.eyJJRCI6MSwibmlja25hbWUiOiJGZW5na2UifQ.wI1mi-WSBxAcLP5Xku3Y0U-TAKUc5BTlsBaB87aiSn1tW8MMhpYOWoOkkMElPk58Pc8_MQ76YQ2IPgp7yxdcj').data
    print(token)
