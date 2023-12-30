# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/3 10:36
@Auth ： 冯珂
@File ：NoteService.py
@IDE ：PyCharm
@Motto: 
"""
from sqlalchemy import or_, desc, func

from app_run.libs.enums import IsDeleteEnum, NoteStateEnum
from app_run.libs.error_code import ClientRedoError, Success, ClientTypeError, NotFound
from app_run.models.base import db
from app_run.models.note_article import NoteArticle
from app_run.models.note_type import NoteType
from app_run.services.Base import BaseService


class NoteService(BaseService):
    def __init__(self):
        super().__init__()
        self.user = self.get_user_dic()

    def home_page(self):
        """
        home_page首页获取
        """
        data = self.get_form_data()
        page = int(data.get('page', 0))
        size = int(data.get('size', 20))
        with db.auto_commit():
            note_query = db.session.query(NoteArticle.id,
                                          NoteArticle.type_id,
                                          NoteArticle.note_title,
                                          NoteArticle.note_tags,
                                          NoteArticle.note_cover,
                                          NoteArticle.note_abstract,
                                          NoteArticle.note_html,
                                          NoteArticle.note_md,
                                          NoteArticle.like_amount,
                                          NoteArticle.create_time).\
                filter(NoteArticle.is_delete == 0).\
                order_by(desc(NoteArticle.create_time)).\
                offset(page * size).\
                limit(size).all()
            note_list = self.query_to_list(note_query)

            count_query = db.session(func.count(NoteArticle.id)). \
                filter(NoteArticle.is_delete == 0).first()
            count = count_query[0] if count_query else 0

            data_inform = {
                'count': count,
                'note_list': note_list
            }
        return Success(data=data_inform)

    def note_type_add(self):
        """
        增加文章分类
        :return:
        """
        with db.auto_commit():
            data = self.get_data()
            # 校验文章分类名称冲突
            note_type_query = db.session.query(NoteType). \
                filter(NoteType.user_id == self.user.get('user_id')). \
                filter(NoteType.type_name == data.get('type_name')). \
                filter(NoteType.is_delete == IsDeleteEnum.未删除.value).first()
            if note_type_query:
                raise ClientRedoError(msg='文章分类你已经有了哟！')

            # 添加文章分类
            note_type_obj = NoteType()
            note_type_obj.user_id = self.user.get('user_id')
            note_type_obj.user_name = self.user.get('user_name')
            note_type_obj.type_name = data.get('type_name')
            note_type_obj.type_intro = data.get('type_intro')
            note_type_obj.type_cover = data.get('type_cover') if data.get('type_cover', None) else 6
            db.session.add(note_type_obj)

            return Success()

    def note_type_get(self):
        """
        获取笔记分类
        :return:
        """
        with db.auto_commit():
            args = self.get_args()
            condition = [NoteType.user_id == self.user.get('user_id'),
                         NoteType.is_delete == IsDeleteEnum.未删除.value]
            select = args.get('select', None)
            if select:
                condition.append(or_(NoteType.type_name.like('%' + select + '%'),
                                     NoteType.type_intro.like('%' + select + '%')))

            note_type_query = db.session.query(NoteType.id,
                                               NoteType.type_name,
                                               NoteType.type_intro,
                                               NoteType.type_cover,
                                               NoteType.is_top,
                                               NoteType.create_time). \
                filter(*condition). \
                order_by(-NoteType.is_top, -NoteType.create_time).all()

            note_type_data = self.query_to_list(note_type_query)
            return Success(data=note_type_data)

    def note_type_update(self):
        """
        修改笔记分类
        :return:
        """
        with db.auto_commit():
            data = self.get_data()
            # 校验文章分类名称冲突
            note_type_query = db.session.query(NoteType). \
                filter(NoteType.user_id == self.user.get('user_id')). \
                filter(NoteType.id != data.get('type_id')). \
                filter(NoteType.type_name == data.get('type_name')). \
                filter(NoteType.is_delete == IsDeleteEnum.未删除.value).first()
            if note_type_query:
                raise ClientRedoError(msg='文章分类你已经有了哟！')

            # 修改信息
            up_data = {}
            if data.get('type_name'):
                up_data[NoteType.type_name] = data.get('type_name')
            if data.get('type_cover'):
                up_data[NoteType.type_cover] = data.get('type_cover')
            if data.get('type_intro'):
                up_data[NoteType.type_intro] = data.get('type_intro')

            db.session.query(NoteType). \
                filter(NoteType.user_id == self.user.get('user_id')). \
                filter(NoteType.id == data.get('type_id')). \
                update(up_data)

            return Success()

    def note_type_delete(self):
        """
        删除笔记分类
        :return:
        """
        with db.auto_commit():
            type_id = self.get_data(key='type_id')
            # 校验该分类下有无文章
            item_query = db.session.query(NoteArticle). \
                filter(NoteArticle.type_id == type_id). \
                filter(NoteArticle.is_delete == IsDeleteEnum.未删除.value).first()
            if item_query:
                raise ClientRedoError(msg='该分类下存在有效文章，无法删除该分类！')

            # 删除分类
            db.session.query(NoteType). \
                filter(NoteType.id == type_id). \
                filter(NoteType.user_id == self.user.get('user_id')). \
                update({NoteType.is_delete: IsDeleteEnum.删除.value})

            return Success()

    def note_type_top(self):
        """
        是否置顶
        :return:
        """
        with db.auto_commit():
            data = self.get_data()
            note_type_query = db.session.query(NoteType). \
                filter(NoteType.user_id == self.user.get('user_id')). \
                filter(NoteType.id == data.get('type_id')).first()
            if note_type_query is None:
                raise NotFound()
            note_type_query.is_top = data.get('is_top')

            return Success()

    def note_article_add(self):
        """
        添加笔记
        :return:
        """
        with db.auto_commit():
            data = self.get_data()
            # if data.get('state') and data.get('state') not in [0, 1]:
            #     raise ClientTypeError(msg='提交状态错误！')

            # 查看名称重复不
            article_query = db.session.query(NoteArticle). \
                filter(NoteArticle.user_id == self.user.get('user_id')). \
                filter(NoteArticle.is_delete == IsDeleteEnum.未删除.value). \
                filter(NoteArticle.type_id == data.get('type_id') if data.get('type_id') else True). \
                filter(NoteArticle.note_title == data.get('note_title')).first()
            if article_query:
                raise ClientRedoError(msg='存在重复标题，请修改！')

            article_obj = NoteArticle()
            article_obj.type_id = data.get('type_id') if data.get('type_id') else 0
            article_obj.note_title = data.get('note_title')
            article_obj.note_tags = ';'.join(data.get('note_tags'))
            article_obj.note_cover = data.get('note_cover')
            article_obj.note_abstract = data.get('note_abstract')
            article_obj.note_html = data.get('note_html')
            article_obj.note_md = data.get('note_md')
            # article_obj.state = data.get('state') if data.get('state') else NoteStateEnum.草稿.value
            article_obj.state = NoteStateEnum.审核通过.value
            article_obj.user_id = self.user.get('user_id')
            article_obj.user_name = self.user.get('user_name')
            db.session.add(article_obj)

            return Success()

    def note_catalogue_get(self):
        """
        获取文章目录
        :return:
        """
        with db.auto_commit():
            type_query = db.session.query(NoteType.id,
                                          NoteType.type_name,
                                          NoteType.type_cover). \
                filter(NoteType.user_id == self.user.get('user_id')). \
                filter(NoteType.is_delete == IsDeleteEnum.未删除.value). \
                order_by(-NoteType.is_top, -NoteType.create_time).all()
            type_data_list = self.query_to_list(type_query)
            for v in type_data_list:
                article_query = db.session.query(NoteArticle.id,
                                                 NoteArticle.note_title). \
                    filter(NoteArticle.type_id == v.get('id')). \
                    filter(NoteArticle.user_id == self.user.get('user_id')). \
                    filter(NoteArticle.is_delete == IsDeleteEnum.未删除.value). \
                    order_by(NoteArticle.create_time).all()
                v['article_data'] = self.query_to_list(article_query)
            return Success(data=type_data_list)

    def note_article_get(self):
        """
        获取文章笔记
        :return:
        """
        with db.auto_commit():
            data = self.get_args()
            article_query = db.session.query(NoteArticle.id,
                                             NoteArticle.note_title,
                                             NoteArticle.note_tags,
                                             NoteArticle.note_cover,
                                             NoteArticle.note_abstract,
                                             NoteArticle.note_html,
                                             NoteArticle.note_md,
                                             NoteArticle.state,
                                             NoteArticle.create_time). \
                filter(NoteArticle.id == data.get('article_id')). \
                filter(NoteArticle.user_id == self.user.get('user_id')). \
                filter(NoteArticle.is_delete == IsDeleteEnum.未删除.value).first()
            article_data = self.query_to_dict(article_query)
            article_data['note_tags'] = article_data['note_tags'].split(';')

            return Success(data=article_data)

    def note_article_update(self):
        """
        修改文章
        :return:
        """
        with db.auto_commit():
            data = self.get_data()
            # 审核中和审核完成文章不允许修改
            article_query = db.session.query(NoteArticle). \
                filter(NoteArticle.user_id == self.user.get('user_id')). \
                filter(NoteArticle.id == data.get('article_id')).first()
            if article_query is None:
                raise NotFound()
            # elif article_query.state in [NoteStateEnum.审核中.value, NoteStateEnum.审核通过.value]:
            #     raise ClientTypeError(msg='该文章状态不允许做修改操作！')
                # 校验
            article_query = db.session.query(NoteArticle). \
                filter(NoteArticle.user_id == self.user.get('user_id')). \
                filter(NoteArticle.id != data.get('article_id')). \
                filter(NoteArticle.is_delete == IsDeleteEnum.未删除.value). \
                filter(NoteArticle.type_id == data.get('type_id') if data.get('type_id') else True). \
                filter(NoteArticle.note_title == data.get('note_title')).first()
            if article_query:
                raise ClientRedoError(msg='存在重复标题，请修改！')

            db.session.query(NoteArticle).\
                filter(NoteArticle.user_id == self.user.get('user_id')). \
                filter(NoteArticle.id == data.get('article_id')).\
                update({NoteArticle.type_id: data.get('type_id'),
                        NoteArticle.note_title: data.get('note_title'),
                        NoteArticle.note_tags: ';'.join(data.get('note_tags')),
                        NoteArticle.note_cover: data.get('note_cover'),
                        NoteArticle.note_abstract: data.get('note_abstract'),
                        NoteArticle.note_html: data.get('note_html'),
                        NoteArticle.note_md: data.get('note_md')})

            return Success()

    def note_article_delete(self):
        """
        删除文章
        :return:
        """
        with db.auto_commit():
            data = self.get_data()
            article_query = db.session.query(NoteArticle). \
                filter(NoteArticle.user_id == self.user.get('user_id')). \
                filter(NoteArticle.id == data.get('article_id')).first()
            if article_query is None:
                raise NotFound()
            elif article_query.state in [NoteStateEnum.审核中.value]:
                raise ClientTypeError(msg='该文章状态不允许做删除操作！')

            db.session.query(NoteArticle). \
                filter(NoteArticle.user_id == self.user.get('user_id')). \
                filter(NoteArticle.id == data.get('article_id')). \
                update({NoteArticle.is_delete: IsDeleteEnum.删除.value})

            return Success

    def note_article_revocation(self):
        """
        撤回文章
        :return:
        """
        with db.auto_commit():
            data = self.get_data()
            article_query = db.session.query(NoteArticle). \
                filter(NoteArticle.user_id == self.user.get('user_id')). \
                filter(NoteArticle.id == data.get('article_id')).first()
            if article_query is None:
                raise NotFound()

            db.session.query(NoteArticle). \
                filter(NoteArticle.user_id == self.user.get('user_id')). \
                filter(NoteArticle.id == data.get('article_id')). \
                update({NoteArticle.state: NoteStateEnum.草稿.value})

            return Success()
