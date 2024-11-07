#!/usr/bin/env python3
"Encrypting passwords"
import bcrypt


def hash_password(password: str) -> bytes:
    "hash a password using bcrypt"
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    "check if password is valid"
    return bcrypt.checkpw(password.encode(), hashed_password)
