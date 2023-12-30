from app_run.models.base import db

if __name__ == '__main__':
    from app_run import app
    with app.app_context(), db.auto_commit():
        query = db.session


