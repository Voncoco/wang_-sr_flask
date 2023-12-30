# coding=utf-8
from datetime import datetime
import time
from app.models.base import db
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, SMALLINT, BigInteger, Float, TEXT, Date
from sqlalchemy.dialects.mysql import LONGTEXT


class PcUser(db.Model):
    '''
    模型(表)备注:
   用户表
    '''
    __tablename__ = 'pc_user'

    '''   主键ID   '''
    id = Column(BigInteger(), primary_key=True)

    '''   登录名   '''
    nickname = Column(String(24), nullable=False)

    '''   电话号码   '''
    phone = Column(String(64))

    '''   加密密码   '''
    password = Column(String(500))

    '''   随机字符串   '''
    stochastic = Column(String(100))

    '''   邮箱   '''
    Email = Column(String(50))

    '''   性别（0：女，1：男）   '''
    gender = Column(Integer())

    '''   创建时间   '''
    create_time = Column(DateTime(), default=datetime.now)

    '''   是否可以上传文件（0：不可以，1：可以）   '''
    is_IO = Column(Integer(), nullable=False)

    '''   是否停用（0：未停用，1：停用）   '''
    is_disable = Column(Integer())

    '''   是否删除（0：未删除，1：删除）   '''
    is_delete = Column(Integer())

    '''   logo   '''
    logo = Column(BigInteger())

    '''   附带信息   '''
    incidental = Column(LONGTEXT)

