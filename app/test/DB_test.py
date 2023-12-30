from app.models.base import db

if __name__ == '__main__':
    from app import app
    with app.app_context(), db.auto_commit():
        query = db.session


