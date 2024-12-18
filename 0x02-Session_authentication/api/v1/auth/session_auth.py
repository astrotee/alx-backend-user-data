#!/usr/bin/env python3
"Session Authentication"
from typing import Dict, Any
from uuid import uuid4
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    "Session Authentication"
    user_id_by_session_id: Dict[str, Any] = {}

    def create_session(self, user_id: str = None) -> str:
        "create a user session"
        if user_id is None or not isinstance(user_id, str):
            return None
        id = str(uuid4())
        SessionAuth.user_id_by_session_id[id] = user_id
        return id

    def destroy_session(self, request=None):
        "delete a session"
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user = self.user_id_for_session_id(session_id)
        if user is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True

    def user_id_for_session_id(self, session_id: str = None) -> str:
        "get the user_id of a session"
        if session_id is None or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        "get the current user"
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)
