#!/usr/bin/env python3
"Session Authentication with expiration"
from datetime import datetime, timedelta
from os import getenv
from flask import request

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    "Session Authentication with expiration"
    def __init__(self) -> None:
        super().__init__()
        if getenv('SESSION_DURATION', '').isdigit():
            self.session_duration = int(getenv('SESSION_DURATION', ''))
        else:
            self.session_duration = 0

    def create_session(self, user_id=None):
        "create a user session"
        id = super().create_session(user_id)
        if id is None:
            return None
        SessionAuth.user_id_by_session_id[id] = {'user_id': user_id,
                                                 'created_at': datetime.now()
                                                 }
        return id

    def user_id_for_session_id(self, session_id=None):
        "get the user_id of a session"
        if session_id is None or not isinstance(session_id, str):
            return None
        session = SessionAuth.user_id_by_session_id.get(session_id)
        if session is None:
            return None
        if self.session_duration <= 0:
            return session['user_id']
        if 'created_at' not in session:
            return None
        if (session['created_at']
                + timedelta(seconds=self.session_duration)) < datetime.now():
            return None
        return session['user_id']
