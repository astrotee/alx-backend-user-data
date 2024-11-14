#!/usr/bin/env python3
""" Session Authentication views
"""
from os import getenv
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /api/v1/auth_session/login
    Return:
      - login status
    """
    email = request.form.get('email')
    pwd = request.form.get('password')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if pwd is None:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user: User = users[0]
    if not user.is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    res = jsonify(user.to_json())
    res.set_cookie(getenv('SESSION_NAME', '_my_session_id'), session_id)
    return res


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ DELETE /api/v1/auth_session/logout
    Return:
      - logout status
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({})
    abort(404)
