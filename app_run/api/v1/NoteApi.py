# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/3 10:30
@Auth ： 冯珂
@File ：NoteApi.py
@IDE ：PyCharm
@Motto: 
"""
from flask import render_template

from Tool.decorate import request_check
from app_run.libs.redprint import Redprint
from app_run.services.Note.NoteService import NoteService
from app_run.validators.forms import NoteTypeAddForm, NoteTypeUpdateForm, NoteTypeDeleteForm, NoteArticleAddForm, \
    NoteArticleGetForm, NoteArticleUpdateForm, NoteTypeTopForm

api = Redprint('note')


@api.route('/home/page', methods=['GET', 'POST'])
@request_check
def home_page():
    """
    首页获取笔记
    """
    res = NoteService()
    data_inform = res.home_page().data
    return render_template('home_page.html', data=data_inform)


@api.route('/type/add', methods=['POST'])
@request_check
def type_add():
    """
    增加笔记分类
    :return:
    """
    NoteTypeAddForm().validate_for_api()
    res = NoteService()
    return res.note_type_add()


@api.route('/type/get', methods=['GET'])
@request_check
def type_get():
    """
    获取笔记分类
    :return:
    """
    res = NoteService()
    return res.note_type_get()


@api.route('/type/update', methods=['PUT'])
@request_check
def type_update():
    """
    修改笔记分类
    :return:
    """
    NoteTypeUpdateForm().validate_for_api()
    res = NoteService()
    return res.note_type_update()


@api.route('/type/delete', methods=['DELETE'])
@request_check
def type_delete():
    """
    删除笔记分类
    :return:
    """
    NoteTypeDeleteForm().validate_for_api()
    res = NoteService()
    return res.note_type_delete()


@api.route('/type/top', methods=['PUT'])
@request_check
def type_top():
    """
    是否置顶
    :return:
    """
    NoteTypeTopForm().validate_for_api()
    res = NoteService()
    return res.note_type_top()


@api.route('/article/add', methods=['POST'])
@request_check
def article_add():
    """
    添加笔记
    :return:
    """
    NoteArticleAddForm().init_and_validate()
    res = NoteService()
    return res.note_article_add()


@api.route('/catalogue/get', methods=['GET'])
@request_check
def catalogue_get():
    """
    获取文章目录
    :return:
    """
    res = NoteService()
    return res.note_catalogue_get()


@api.route('/article/get', methods=['GET'])
@request_check
def article_get():
    """
    获取文章
    :return:
    """
    NoteArticleGetForm().validate_for_api()
    res = NoteService()
    return res.note_article_get()


@api.route('/article/update', methods=['PUT'])
@request_check
def article_update():
    """
    修改文章
    :return:
    """
    NoteArticleUpdateForm().init_and_validate()
    res = NoteService()
    return res.note_article_update()


@api.route('/article/delete', methods=['DELETE'])
@request_check
def article_delete():
    """
    删除文章
    :return:
    """
    NoteArticleGetForm().validate_for_api()
    res = NoteService()
    return res.note_article_delete()


@api.route('/article/revocation', methods=['POST'])
@request_check
def article_revocation():
    """
    撤回文章
    :return:
    """
    NoteArticleGetForm().validate_for_api()
    res = NoteService()
    return res.note_article_revocation()
