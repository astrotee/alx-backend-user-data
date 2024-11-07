#!/usr/bin/env python3
"Regex-ing"
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    "filte sensitive fields"
    return re.sub(f"({'|'.join(fields)})=.*?{separator}",
                  rf"\1={redaction}{separator}", message)
