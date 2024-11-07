#!/usr/bin/env python3
"Encrypting passwords"
import bcrypt


def hash_password(password: str) -> bytes:
    "hash a password using bcrypt"
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
