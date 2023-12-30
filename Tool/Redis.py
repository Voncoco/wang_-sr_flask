import redis
from config.secure import RedisConfig


class Redis:
    def __init__(self, db='HWY_1_setting'):
        self.db = db
        self.RedisC = RedisConfig[db]
        self.pool = redis.ConnectionPool(host=self.RedisC['host'],
                                         port=self.RedisC['port'],
                                         password=self.RedisC['password'],
                                         db=self.RedisC['db'],
                                         max_connections=100)  # 最多连接数量
        self.conn = redis.Redis(connection_pool=self.pool)

    # 存
    def set_str(self, mobile, codes, time=0):
        if time == 0:
            self.conn.set(mobile, codes)
        else:
            self.conn.setex(mobile, time, codes)

    # 取
    def get_str(self, mobile):
        value = self.conn.get(mobile)
        if value:
            value = str(value, encoding='utf8')
        return value

    # 删
    def del_str(self, mobile):
        self.conn.delete(mobile)

    # 存集合
    def insert_set(self, key, value):
        for i in value:
            self.conn.sadd(key, i)

    # 取集合
    def find_set(self, key):
        value = self.conn.smembers(key)
        if value:
            list = []
            for i in value:
                list.append(str(i, encoding='utf8'))
            return list
        else:
            return None

    # 存 hash   params是小key
    def hash_set(self, key, params, value):
        self.conn.hset(key, params, value)

    # 获取某个值
    def get_one(self, key, params):
        return self.conn.hget(key, params)

    # 取所有值
    def get_all(self, key):
        return self.conn.hgetall(key)

    # 删除某个
    def del_hash(self, key, params):
        self.conn.hdel(key, params)


if __name__ == '__main__':
    r = Redis()
    a = r.get_str('age')
    print(a)