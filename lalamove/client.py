import httpx
import json
import uuid
from typing import Optional, Dict
from lalamove.auth import get_auth_token
from lalamove.constants import ENDPOINTS, MARKETS
from lalamove.utils import convert_keys_to_camel_case
from lalamove.errors import (
    BadRequest,
    Unauthorized,
    PaymentRequired,
    Forbidden,
    NotFound,
    InsufficientStops,
    OrderNotFound,
    InvalidField,
    MissingField,
    TooManyStops,
    InvalidQuotationID,
    TooManyRequests,
    InternalServerError,
)

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

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None):
        if endpoint not in ENDPOINTS:
            raise ValueError(f"Invalid endpoint: {endpoint}")

        if method.upper() not in ENDPOINTS.get(endpoint, []):
            raise ValueError(f"Invalid method for endpoint {endpoint}: {method}")

        data = convert_keys_to_camel_case(data)

        token = get_auth_token(
            method.upper(), endpoint, json.dumps(data), self.api_key, self.api_secret
        )

        headers = {
            "Authorization": f"Bearer {token}",
            "Market": self.market,
            "Request-ID": str(uuid.uuid4()),
        }

        url = f"{self.base_url}/{endpoint}"

        return httpx.request(method, url, headers=headers, json=data)

    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None):
        try:
            response = self._make_request(method, endpoint, data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as error:
            error_data = error.response.json()

            match error.status_code:
                case 400:
                    raise BadRequest
                case 401:
                    raise Unauthorized
                case 402:
                    raise PaymentRequired
                case 403:
                    raise Forbidden
                case 404:
                    raise NotFound
                case 422 if error_data.get("message") == "ERR_INSUFFICIENT_STOPS":
                    raise InsufficientStops
                case 422 if error_data.get("message") == "ERR_ORDER_NOT_FOUND":
                    raise OrderNotFound
                case 422 if error_data.get("message") == "ERR_INVALID_FIELD":
                    raise InvalidField
                case 422 if error_data.get("message") == "ERR_MISSING_FIELD":
                    raise MissingField
                case 422 if error_data.get("message") == "ERR_TOO_MANY_STOPS":
                    raise TooManyStops
                case 422 if error_data.get("message") == "ERR_INVALID_QUOTATION_ID":
                    raise InvalidQuotationID
                case 429:
                    raise TooManyRequests
                case 500:
                    raise InternalServerError
                case _:
                    raise error
