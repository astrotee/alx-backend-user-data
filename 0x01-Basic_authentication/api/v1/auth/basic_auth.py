#!/usr/bin/env python3
"Basic Authentication"
from base64 import b64decode
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    "Basic Authentication"

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        "exctract the value of the authorization header"
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.removeprefix('Basic ')

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        "returns the decoded value of a Base64 string"
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> Tuple[str, str]:
        "returns the user email and password from the Base64 decoded value"
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        "returns the User instance based on his email and password"
        if user_email is None or user_pwd is None:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if len(users) == 0:
            return None
        user: User = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        "get the current user"
        authorization_header = self.authorization_header(request)
        b64_header = self.extract_base64_authorization_header(
            authorization_header
        )
        str_header = self.decode_base64_authorization_header(b64_header)
        user_email, user_pwd = self.extract_user_credentials(str_header)
        return self.user_object_from_credentials(user_email, user_pwd)
