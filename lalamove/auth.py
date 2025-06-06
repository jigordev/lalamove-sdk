import hmac
import hashlib
import time
from typing import Literal, Optional

HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]


def get_signature(method: HttpMethod, path: str, body: str, secret: str):
    timestamp = str(int(time.time() * 1000))
    message = f"{timestamp}\r\n{method}\r\n{path}\r\n\r\n{body}"
    result = hmac.new(secret.encode(), message.encode(), hashlib.sha256)
    return timestamp, result.hexdigest()


def get_auth_token(
    api_key: str,
    api_secret: str,
    method: HttpMethod,
    path: str,
    body: Optional[str] = "",
):
    timestamp, signature = get_signature(method, path, body, api_secret)
    return f"{api_key}:{timestamp}:{signature}"
