# coding=utf-8
from datetime import datetime
import time
from app.models.base import db
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, SMALLINT, BigInteger, Float, TEXT, Date
from sqlalchemy.dialects.mysql import LONGTEXT


class NoteType(db.Model):
    """
    模型(表)备注:
    笔记分类
    """
    __tablename__ = 'note_type'

    # 主键
    id = Column(BigInteger(), primary_key=True)

    # 文章类型名称
    type_name = Column(String(64), nullable=True)

    # 文章类型简介
    type_intro = Column(String(255), nullable=True)

    # 文章类型封面图片ID
    type_cover = Column(BigInteger(), nullable=True)

    # 用户ID
    user_id = Column(BigInteger(), nullable=False)

    # 用户名称
    user_name = Column(String(32), nullable=True)

    # 创建时间
    create_time = Column(DateTime(), default=datetime.now(), nullable=True)

    # 是否删除（0：未删除，1：删除）
    is_delete = Column(Integer(), nullable=True, default=0)

    # 是否置顶（0：未置顶，1：置顶）
    is_top = Column(Integer(), nullable=True, default=0)

