
from flask import jsonify

from Tool.decorate import file_bmp, request_check
from app.libs.redprint import Redprint
from app.services.File.FileService import FileService, down_file
from app.validators.forms import FileGet

api = Redprint('files')


@api.route('/upload', methods=['POST'])
@request_check
@file_bmp
def upload():
    """
    上传文件
    """
    res = FileService()
    return res.upload()


@api.route('/delete', methods=['DELETE'])
@request_check
def file_delete():
    """
    文件删除
    :return:
    """
    res = FileService()
    return res.delete()


@api.route('/<filename>')
def get_files(filename):
    """
    下载文件
    """
    return down_file(filename=filename)


@api.route('/get', methods=['GET'])
def file_get():
    """
    获取文件URL
    :return:
    """
    form = FileGet().validate_for_api()
    res = FileService()
    return res.file_get(file_id=form.file_id.data)
