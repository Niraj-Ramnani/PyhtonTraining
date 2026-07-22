import re


def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))


def validate_phone_number(phone):
    pattern = r'^\d{10}$'
    return bool(re.match(pattern, phone))