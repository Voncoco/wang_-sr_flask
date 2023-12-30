# coding=utf-8
from datetime import datetime
import time
from app.models.base import db
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, SMALLINT, BigInteger, Float, TEXT, Date


class PcFile(db.Model):
    '''
    模型(表)备注:
上传文件信息表
    '''
    __tablename__ = 'pc_file'

    '''   主键ID   '''
    id = Column(Integer(), primary_key=True)

    '''   用户ID   '''
    user_id = Column(Integer(), nullable=False)

    '''   文件原始名称   '''
    name = Column(String(50))

    '''   文件时间戳   '''
    name_tag = Column(String(100), nullable=False)

    '''   文件类型   '''
    type = Column(String(11), nullable=False)

    '''   文件大小   '''
    size = Column(Float)

    '''   文件相对路径   '''
    path = Column(String(50), nullable=False)

    '''   文件创建时间   '''
    creat_time = Column(DateTime(), default=datetime.now, nullable=False)

    '''   是否删除（0：否，1：是）   '''
    is_delete = Column(Integer(), default=0, nullable=False)

    def keys(self):
        return ['id', 'user_id', 'name', 'name_tag', 'type', 'size', 'path', 'creat_time', 'is_delete']

    def __repr__(self):
        return "pc_file(id='{self.id}',user_id='{self.user_id}',name='{self.name}',name_tag='{self.name_tag}',type='{self.type}',size='{self.size}',path='{self.path}',creat_time='{self.creat_time}',is_delete='{self.is_delete}')".format(self=self)