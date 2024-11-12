#!/usr/bin/env python3
"Basic Authentication"
from base64 import b64decode
from api.v1.auth.auth import Auth


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
