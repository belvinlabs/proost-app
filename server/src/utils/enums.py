from enum import Enum, unique


@unique
class APIErrorTypes(Enum):
    user_not_found = 1
    user_already_exists = 2
    database_already_exists = 3
    invalid_email = 4
