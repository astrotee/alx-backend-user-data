#!/usr/bin/env python3
"Authentication"
from typing import List, TypeVar
from flask import request


class Auth:
    "Authentication"

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        "check if Authentication is required"
        return False

    def authorization_header(self, request=None) -> str:
        "get the authoriztation header"
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        "get current user"
        return None
