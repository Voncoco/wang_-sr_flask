# coding=utf-8
from datetime import datetime
import time
from app.models.base import db
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, SMALLINT, BigInteger, Float, TEXT, Date
from sqlalchemy.dialects.mysql import LONGTEXT


class NoteArticle(db.Model):
    """
    模型(表)备注:
    文章信息
    """
    __tablename__ = 'note_article'

    # 主键ID
    id = Column(BigInteger(), primary_key=True)

    # 分类ID
    type_id = Column(BigInteger(), nullable=True)

    # 文章标题
    note_title = Column(String(64), nullable=False)

    # 标签
    note_tags = Column(String(64), nullable=False)

    # 文章封面
    note_cover = Column(BigInteger(), nullable=True)

    # 文章摘要
    note_abstract = Column(String(128), nullable=True)

    # html文本
    note_html = Column(LONGTEXT, nullable=True)

    # md文本
    note_md = Column(LONGTEXT, nullable=True)

    # 点赞数量
    like_amount = Column(BigInteger(), nullable=True, default=0)

    # 状态（0：草稿，1：审核中，2：审核通过，3：审核未通过）
    state = Column(Integer(), nullable=True, default=0)

    # 用户ID
    user_id = Column(BigInteger(), nullable=True)

    # 用户名称
    user_name = Column(String(32), nullable=True)

    # 创建时间
    create_time = Column(DateTime(), default=datetime.now(), nullable=True)

    # 是否删除（0：未删除，1：删除）
    is_delete = Column(Integer(), nullable=True, default=0)

