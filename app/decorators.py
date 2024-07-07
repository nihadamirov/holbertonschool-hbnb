from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import request, jsonify
from app.models.user import User

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            if current_user.role.name != role:
                return jsonify({"msg": "You do not have access to this resource"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
