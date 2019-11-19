import re

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


def is_email(val):
    return re.match(EMAIL_REGEX, val) is not None


def is_int(val):
    if val[0] in ('-', '+'):
        return val[1:].isdigit()
    return val.isdigit()
