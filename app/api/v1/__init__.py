from flask import Blueprint
from app.api.v1 import UserApi
from app.api.v1 import NoteApi


def create_blueprint_v1():
    """实例化蓝图"""
    bp_v1 = Blueprint('v1', __name__)
    UserApi.api.register(bp_v1)
    NoteApi.api.register(bp_v1)
    return bp_v1
