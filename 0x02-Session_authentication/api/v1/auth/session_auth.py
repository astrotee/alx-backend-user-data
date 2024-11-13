#!/usr/bin/env python3
"Session Authentication"
from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    "Session Authentication"
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        "create a user session"
        if user_id is None or not isinstance(user_id, str):
            return None
        id = str(uuid4())
        SessionAuth.user_id_by_session_id[id] = user_id
        return id
