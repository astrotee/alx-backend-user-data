#!/usr/bin/env python3
"basic Flask app"
from flask import Flask, abort, jsonify, redirect, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def main():
    "main route"
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    "register users"
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/login", methods=["POST"])
def login():
    """User Login with creds
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or\
            password is None or\
            not AUTH.valid_login(email, password):
        abort(401)
    sid = AUTH.create_session(email)
    if sid is None:
        abort(401)
    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie("session_id", sid)
    return res


@app.route("/sessions", methods=["DELETE"])
def logout():
    """User Logout
    """
    session_id = request.cookies.get("session_id")

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
