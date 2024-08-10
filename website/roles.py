from enum import Enum
from functools import wraps
from flask import abort
from flask_login import current_user

class Role(Enum):
    User = 0
    TeamMember = 1
    Admin = 2

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role < role.value:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator
