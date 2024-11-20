#!/usr/bin/env python3
"Auth utils"
from typing import Optional
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    "return the salted hash of a password"
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ generate a uuid str
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a new user
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password).decode())
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """check if the creds are valid
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(),
                                  user.hashed_password.encode())
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Optional[str]:
        """ create a user session
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        sid = _generate_uuid()
        self._db.update_user(user.id, session_id=sid)
        return sid
