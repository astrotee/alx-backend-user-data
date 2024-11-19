#!/usr/bin/env python3
"Auth utils"
import bcrypt


def _hash_password(password: str) -> bytes:
    "return the salted hash of a password"
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
