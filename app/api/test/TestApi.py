# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/3 10:54
@Auth ： 冯珂
@File ：TestApi.py
@IDE ：PyCharm
@Motto: 
"""

from app.libs.error_code import Success
from app.libs.redprint import Redprint

api = Redprint('test')


@api.route('/update', methods=['POST'])
def test_update():
    return Success(data={})

