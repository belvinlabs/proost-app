from sqlalchemy.orm.exc import NoResultFound

from utils.enums import APIErrorTypes
from utils.validators import is_email
from models.app_main import User


from utils.errors import APIError


def get_user_email(email):
    if not is_email(email):
        raise APIError(
            http_code=409,
            error_type_key=APIErrorTypes.user_not_found,
            message=f'Invalid ID supplied. {email} is not a valid ID nor a '
                    f'valid email address'
        )

    try:
        return User.query.filter_by(email=email).one()
    except NoResultFound:
        raise APIError(
            http_code=404,
            error_type_key=APIErrorTypes.user_not_found,
            message=f'Can\'t find a user with the email {email}'
        )


def get_user_id(id):
    try:
        return User.query.filter_by(id=id).one()
    except NoResultFound:
        raise APIError(
            http_code=404,
            error_type_key=APIErrorTypes.user_not_found,
            message=f'Can\'t find a user with the id {id}'
        )
