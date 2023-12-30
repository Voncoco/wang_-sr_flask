"""
定时任务
"""
from app_run.libs.enums import FileTypeEnum


def Generate_file(app):
    """
    定时任务：生成指定格式文件的文件夹
    """
    import os
    from flask import current_app
    with app.app_context():
        serve_path = current_app.root_path  # 获取项目路径
        file_type_list = [v.name.lower() for v in FileTypeEnum]  # 获取允许文件格式列表
        for v in file_type_list:
            file_path = serve_path + '/Document/' + str(v)  # 文件目录路径
            if os.path.exists(file_path):
                pass
            else:
                print('创建了文件夹{}'.format(v))
                os.mkdir(file_path)
