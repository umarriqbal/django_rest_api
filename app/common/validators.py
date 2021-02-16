
from .custom_exceptions import InvalidPasswordError


def password_validator(pwd_str):

    contains_digit = any(map(str.isdigit, pwd_str))
    if not contains_digit:
        raise InvalidPasswordError('Password must have integers.')

    contains_alphabet = any(map(str.isalpha, pwd_str))
    if not contains_alphabet:
        raise InvalidPasswordError('Password must have alphabets.')

