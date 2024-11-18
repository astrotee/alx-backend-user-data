#!/usr/bin/env python3
"Session DB Authentication"
from datetime import datetime, timedelta
from uuid import uuid4
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    "Session DB Authentication"

    def create_session(self, user_id: str = None) -> str:
        "create a user session"
        if user_id is None or not isinstance(user_id, str):
            return None
        id = str(uuid4())
        user_session = UserSession(user_id=user_id, session_id=id)
        user_session.save()
        return id

    def destroy_session(self, request=None):
        "delete a session"
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        UserSession.load_from_file()
        user_sessions = UserSession.search({'session_id': session_id})
        if len(user_sessions) == 0:
            return None
        user_session = user_sessions[0]
        if user_session is None:
            return False
        user_session.remove()
        UserSession.save_to_file()
        return True

    def user_id_for_session_id(self, session_id: str = None) -> str:
        "get the user_id of a session"
        if session_id is None or not isinstance(session_id, str):
            return None
        UserSession.load_from_file()
        user_sessions = UserSession.search({'session_id': session_id})
        if len(user_sessions) == 0:
            return None
        user_session = user_sessions[0]
        if self.session_duration <= 0:
            return user_session.user_id
        if (user_session.created_at
                + timedelta(seconds=self.session_duration))\
                < datetime.utcnow():
            return None
        return user_session.user_id
