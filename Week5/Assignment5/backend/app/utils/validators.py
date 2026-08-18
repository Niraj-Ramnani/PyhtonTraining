import re

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email):
    return bool(email) and bool(EMAIL_REGEX.match(email))


def require_fields(data, fields):
    missing = []
    for field in fields:
        value = data.get(field) if data else None
        if value is None or (isinstance(value, str) and value.strip() == ""):
            missing.append(field)
    return missing


def is_positive_number(value):
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


VALID_PAYMENT_METHODS = {"cash", "card", "upi"}


def is_valid_payment_method(method):
    return isinstance(method, str) and method.strip().lower() in VALID_PAYMENT_METHODS

