def register_blueprints(app):
    from app_run.api.v1 import create_blueprint_v1
    from app_run.api.v2 import create_blueprint_v2
    from app_run.api.test import create_blueprint_test
    from app_run.api.web import create_blueprint_web
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')
    app.register_blueprint(create_blueprint_v2(), url_prefix='/v2')
    app.register_blueprint(create_blueprint_test(), url_prefix='/t')
    app.register_blueprint(create_blueprint_web(), url_prefix='/web')


def register_plugin(app):
    from app_run.models.base import db
    # 将db与flask核心对象关联起来
    db.init_app(app)
    with app.app_context():
        db.create_all(app=app)


def Timing_APScheduler(app):
    import portalocker
    import os
    import atexit
    from flask_apscheduler import APScheduler
    # 将定时任务与flask核心对象关联起来
    scheduler = APScheduler()
    file = open("scheduler.lock", "wb")

    def Lock():
        # 上锁
        try:
            # 加排他非阻塞锁, LOCK_EX 排他锁 、LOCK_NB 非阻塞锁
            portalocker.lock(file, portalocker.LOCK_EX | portalocker.LOCK_NB)
            scheduler.init_app(app)
            scheduler.start(paused=app.config['PAUSED'])
        except:
            pass

    def Unlock():
        # 解锁
        portalocker.unlock(file)
        file.close()

    if os.environ.get("FLASK_ENV") == "development":
        # 如果非WERKZEUG 子进程跳过，防止debug模式提前加锁
        if os.environ.get("WERKZEUG_RUN_MAIN"):
            Lock()
    else:
        Lock()
    # 将 func 注册为终止时执行的函数.
    atexit.register(Unlock)


def start_run(app):
    """
    启动时执行的任务
    """
    from app_run.controller.oracle_job import Generate_file
    Generate_file(app)


def create_app():
    from .app import Flask
    from .config.Timing_confi_guration import SchedulerConfig
    from flask_cors import CORS
    app = Flask(__name__)
    # 解决跨域问题
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.config.from_object('app_run.config.secure')
    app.config.from_object('app_run.config.setting')
    app.config.from_object(SchedulerConfig())
    register_blueprints(app)
    register_plugin(app)
    Timing_APScheduler(app)
    start_run(app)
    return app
