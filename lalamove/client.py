import httpx
import json
import uuid
from typing import Optional, Dict
from lalamove.auth import get_auth_token
from lalamove.constants import ENDPOINTS, MARKETS
from lalamove.utils import convert_keys_to_camel_case

DEV_BASE_URL = "https://rest.sandbox.lalamove.com/v3/quotations"
PROD_BASE_URL = "https://rest.lalamove.com/v3/quotations"


class APIClient:
    def __init__(
        self, api_key: str, api_secret: str, market: str, sandbox: bool = False
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.sandbox = sandbox

        self.base_url = DEV_BASE_URL if sandbox else PROD_BASE_URL

        if market in MARKETS:
            self.market = market
        else:
            raise ValueError(f"Invalid market: {market}")

    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None):
        if endpoint not in ENDPOINTS:
            raise ValueError(f"Invalid endpoint: {endpoint}")

        if method.upper() not in ENDPOINTS.get(endpoint, []):
            raise ValueError(f"Invalid method for endpoint {endpoint}: {method}")

        data = convert_keys_to_camel_case(data)

        token = get_auth_token(
            method.upper(), endpoint, json.load(data), self.api_key, self.api_secret
        )

        headers = {
            "Authorization": f"Bearer {token}",
            "Market": self.market,
            "Request-ID": str(uuid.uuid4()),
        }

        url = f"{self.base_url}/{endpoint}"

        return httpx.request(method, url, headers=headers, json=data)
