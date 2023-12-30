from flask import Blueprint

from app.api.v2 import files


def create_blueprint_v2():
    """实例化蓝图"""
    bp_v2 = Blueprint('v2', __name__)
    files.api.register(bp_v2)
    return bp_v2
