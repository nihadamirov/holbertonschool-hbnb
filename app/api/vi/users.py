from flask import Blueprint, request, jsonify, abort
from app.models.user import User
from app.models.data_manager import DataManager

user_api = Blueprint('user_api', __name__)
data_manager = DataManager()

@user_api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('first_name') or not data.get('last_name'):
        abort(400, description="Missing required fields")
    if data_manager.get(data['email'], 'User'):
        abort(409, description="Email already in use")
    user = User(email=data['email'], password=data.get('password', ''), first_name=data['first_name'], last_name=data['last_name'])
    data_manager.save(user)
    return jsonify(user.__dict__), 201

@user_api.route('/users', methods=['GET'])
def get_users():
    users = data_manager.get_all('User')
    return jsonify(users), 200

@user_api.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = data_manager.get(user_id, 'User')
    if not user:
        abort(404, description="User not found")
    return jsonify(user), 200

@user_api.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = data_manager.get(user_id, 'User')
    if not user:
        abort(404, description="User not found")
    user.update(data)
    data_manager.save(user)
    return jsonify(user), 200

@user_api.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = data_manager.get(user_id, 'User')
    if not user:
        abort(404, description="User not found")
    data_manager.delete(user_id, 'User')
    return '', 204
