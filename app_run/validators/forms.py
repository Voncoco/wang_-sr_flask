from wtforms import StringField, validators, RadioField, IntegerField, FieldList
from wtforms.validators import DataRequired, Regexp

from app_run.validators.base import BaseForm, JsonForm


class UserRegisterForm(BaseForm):
    nickname = StringField(validators=[DataRequired(message='登录名不允许为空'),
                                       validators.Length(max=8, min=3, message="用户名长度必须大于%(min)d且小于%(max)d")])
    password = StringField(validators=[DataRequired(message='密码不允许为空'), Regexp(
        regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+-=]).{8,}$',
        message="密码必须包含大小写字母,特殊字符和数字，且长度不低于8位")])
    # password = StringField()
    email = StringField(validators=[DataRequired(message='邮箱不允许为空'), Regexp(
        regex=r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+',
        message="请输入正确的邮箱格式")])
    phone = StringField(validators=[DataRequired(message='电话不允许为空'), Regexp(regex=r'^1\d{10}$', message="输入正确的电话号码！")])
    gender = RadioField(choices=[(0, '女'), (1, '男'), ], validators=[DataRequired(message='性别必选')])


class UserLoginForm(BaseForm):
    nickname = StringField(validators=[DataRequired(message='登录名不允许为空')])
    password = StringField(validators=[DataRequired(message='密码不允许为空')])


class UserUpdateForm(BaseForm):
    userid = IntegerField(validators=[DataRequired(message='用户ID必传项')])
    nickname = StringField(validators=[DataRequired(message='登录名不允许为空'),
                                       validators.Length(max=8, min=3, message="用户名长度必须大于%(max)d且小于%(min)d")])
    email = StringField(validators=[DataRequired(message='邮箱不允许为空'), Regexp(
        regex=r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+',
        message="请输入正确的邮箱格式")])
    phone = StringField(validators=[DataRequired(message='电话不允许为空'), Regexp(regex=r'^1\d{10}$', message="输入正确的电话号码！")])
    is_disable = RadioField(choices=[(0, '为停用'), (1, '停用'), ], validators=[DataRequired(message='是否停用必选')])
    gender = RadioField(choices=[(0, '女'), (1, '男'), ], validators=[DataRequired(message='性别必选项')])
    incidental = StringField()
    logo = IntegerField()


class UserResetPwd(BaseForm):
    password = StringField(validators=[DataRequired(message='密码不允许为空'), Regexp(
        regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+-=]).{8,}$',
        message="密码必须包含大小写字母,特殊字符和数字，且长度不低于8位")])


class FileGet(BaseForm):
    file_id = StringField(validators=[DataRequired(message='图片ID不能为空！')])


class NoteTypeAddForm(BaseForm):
    type_name = StringField(validators=[DataRequired(message='文章分类名称不允许为空！')])
    type_intro = StringField(validators=[DataRequired(message='请随便介绍一下文章简介呗！'),
                                         validators.Length(max=200, min=4, message="文章简介内容需要在4~200字的呢！")])
    type_cover = StringField()


class NoteTypeUpdateForm(BaseForm):
    type_id = IntegerField(validators=[DataRequired(message='分类ID必传项')])
    type_name = StringField(validators=[DataRequired(message='文章分类名称不允许为空！')])
    type_intro = StringField(validators=[DataRequired(message='请随便介绍一下文章简介呗！'),
                                         validators.Length(max=200, min=4, message="文章简介内容需要在4~200字的呢！")])
    type_cover = StringField()


class NoteTypeDeleteForm(BaseForm):
    type_id = IntegerField(validators=[DataRequired(message='分类ID必传项')])


class NoteTypeTopForm(BaseForm):
    type_id = IntegerField(validators=[DataRequired(message='分类ID必传项')])
    is_top = RadioField(choices=[(0, '取消置顶'), (1, '置顶'), ], validators=[DataRequired(message='是否置顶必填项')])


class NoteArticleAddForm(JsonForm):
    type_id = IntegerField()
    note_title = StringField(validators=[DataRequired(message='文章标题必填！')])
    note_tags = FieldList(StringField(), min_entries=1)
    note_cover = IntegerField()
    note_abstract = StringField(validators=[validators.Length(max=100, message="摘要不能超过100字")])
    note_html = StringField()
    note_md = StringField()
    state = IntegerField()


class NoteArticleGetForm(BaseForm):
    article_id = IntegerField(validators=[DataRequired(message='文章ID必传项')])


class NoteArticleUpdateForm(JsonForm):
    article_id = IntegerField(validators=[DataRequired(message='文章ID必传项')])
    type_id = IntegerField()
    note_title = StringField(validators=[DataRequired(message='文章标题必填！')])
    note_tags = FieldList(StringField(), min_entries=1)
    note_cover = IntegerField()
    note_abstract = StringField(validators=[validators.Length(max=100, message="摘要不能超过100字")])
    note_html = StringField()
    note_md = StringField()
    state = IntegerField()
