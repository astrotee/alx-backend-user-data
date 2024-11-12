#!/usr/bin/env python3
"Authentication"
from typing import List, TypeVar
from flask import request


class Auth:
    "Authentication"

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        "check if Authentication is required"
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        "get the authoriztation header"
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        "get current user"
        return None
