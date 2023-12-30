"""
@Project ：wang_-sr_flask 
@File    ：wsgi.py
@IDE     ：PyCharm 
@Auth    ：冯珂
@Time    ：2023/12/30 17:07 
@Function：
"""
from app import app as application, app

if __name__ == '__main__':
    application.run(port=app.config['PORT'], debug=True, host=app.config['HOST'])
