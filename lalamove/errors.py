import httpx


class BadRequest(httpx.HTTPStatusError):
    pass  # 400


class Unauthorized(httpx.HTTPStatusError):
    pass  # 401


class PaymentRequired(httpx.HTTPStatusError):
    pass  # 402


class Forbidden(httpx.HTTPStatusError):
    pass  # 403


class NotFound(httpx.HTTPStatusError):
    pass  # 404


class UnprocessableEntity(httpx.HTTPStatusError):
    pass


class InsufficientStops(httpx.HTTPStatusError):
    pass  # 422


class OrderNotFound(httpx.HTTPStatusError):
    pass  # 422


class InvalidField(httpx.HTTPStatusError):
    pass  # 422


class MissingField(httpx.HTTPStatusError):
    pass  # 422


class TooManyStops(httpx.HTTPStatusError):
    pass  # 422


class InvalidQuotationID(httpx.HTTPStatusError):
    pass  # 422


class TooManyRequests(httpx.HTTPStatusError):
    pass  # 429


class InternalServerError(httpx.HTTPStatusError):
    pass  # 500
