import os
import time

from flask import current_app, send_from_directory, request

from Tool.decorate import asyncz
from app_run.libs.error_code import Success, NotFound
from app_run.models.base import db
from app_run.models.pc_file import PcFile
from app_run.services.Base import BaseService


def down_file(filename):
    """
    从服务器获取已经上传的文件
    """
    with db.auto_commit():
        is_down = request.args.get('is_down', 0)
        file_name = filename.split('.')[0]
        file_query = db.session.query(PcFile).\
            filter(PcFile.is_delete == 0).\
            filter(PcFile.name_tag == file_name).first()
        if file_query is None:
            return NotFound()
        cd_dev = file_query.path  # 文件相对路径
        serve_path = current_app.root_path  # 获取项目路径
        basedir = serve_path + cd_dev  # 获取保存文件的全路径
        if int(is_down) == 1:
            as_attachment = True
        else:
            as_attachment = False
        return send_from_directory(basedir, filename, as_attachment=as_attachment)


class FileService(BaseService):

    def __init__(self):
        super().__init__()
        self.user = {}

    def upload(self):
        """
        文件上传
        """
        with db.auto_commit():
            self.user = self.get_user_dic()
            files = self.get_files(key='files')
            suffix = files.filename.split('.')[-1]  # 获取文件后缀名
            file_name = files.filename.split('.')[0]  # 文件原始名称
            serve_path = current_app.root_path  # 获取项目路径
            cd_dev = '/Document/' + suffix.lower()  # 文件相对路径
            basedir = serve_path + cd_dev  # 获取保存文件的路径
            name_tag = str(int(time.time()))  # 时间戳作为文件名称
            file_path = basedir + '/' + name_tag + '.' + suffix.lower()
            files.save(file_path)
            size = os.path.getsize(file_path)

            # 向数据库写入数据
            file_cls = PcFile()
            file_cls.user_id = self.user.get('user_id')
            file_cls.name = file_name
            file_cls.name_tag = name_tag
            file_cls.type = suffix.lower()
            file_cls.size = size
            file_cls.path = cd_dev
            db.session.add(file_cls)
            db.session.flush()
            file_id = file_cls.id

            url = r'{DOMAIN_NAME}/v2/files/{name_tag}.{suffix}?is_down=0'.\
                format(DOMAIN_NAME=current_app.config['DOMAIN_NAME'], name_tag=name_tag, suffix=suffix.lower())

            data = {
                "file_id": file_id,
                "url": url
            }

            return Success(data=data)

    def delete(self):
        """
        文件删除
        :return:
        """
        with db.auto_commit():
            data = self.get_data()
            file_id = data.get('file_id')
            # 查找文件信息
            file_query = db.session.query(PcFile).\
                filter(PcFile.id == file_id).\
                filter(PcFile.is_delete == 0).first()

            if file_query is None:
                raise NotFound(msg='没有找到该文件')

            file_query.is_delete = 1

            serve_path = current_app.root_path  # 获取项目路径
            cd_dev = file_query.path  # 文件相对路径
            basedir = serve_path + cd_dev + '/' + file_query.name_tag + '.' + file_query.type  # 获取文件的绝对路径
            os.remove(basedir)
            return Success(msg='文件名：{}.{}删除成功！'.format(file_query.name, file_query.type))

    def file_get(self, file_id):
        """
        获取文件信息
        :param file_id:
        :return:
        """
        with db.auto_commit():
            if not file_id:
                return Success(data={})
            # 查找文件信息
            file_query = db.session.query(PcFile). \
                filter(PcFile.id == file_id). \
                filter(PcFile.is_delete == 0).first()

            if file_query is None:
                raise NotFound(msg='没有找到该文件')

            file_data = self.query_to_dict(file_query)
            url = "{DOMAIN_NAME}/v2/files/{name_tag}.{type}".format(DOMAIN_NAME=current_app.config['DOMAIN_NAME'],
                                                                    name_tag=file_data.get('name_tag'),
                                                                    type=file_data.get('type'))
            file_data['url'] = url
            return Success(data=file_data)
