class BadRequest(Exception):
    pass  # 400


class Unauthorized(Exception):
    pass  # 401


class PaymentRequired(Exception):
    pass  # 402


class Forbidden(Exception):
    pass  # 403


class NotFound(Exception):
    pass  # 404


class InsufficientStops(Exception):
    pass  # 422


class OrderNotFound(Exception):
    pass  # 422


class InvalidField(Exception):
    pass  # 422


class MissingField(Exception):
    pass  # 422


class TooManyStops(Exception):
    pass  # 422


class InvalidQuotationID(Exception):
    pass  # 422


class TooManyRequests(Exception):
    pass  # 429


class InternalServerError(Exception):
    pass  # 500
