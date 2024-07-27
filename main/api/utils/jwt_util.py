from datetime import timedelta

from jose import jwt

from main.api.config import settings
from main.api.exceptions.bad_request import BadRequestException
from main.api.exceptions.decode_token import DecodeTokenException
from main.api.user.model.user import User
from main.api.utils.util import now


def generate_token(user: User, is_access: bool = True):
    """
    The function will encode the security token that the client side will send
    in every request inside the header.
    :param user:
    :param is_access:
    :return: False or hash (str)
    """
    if is_access:
        expiration_date = now() + timedelta(minutes=5)
        secret = settings.jwt_access_secret_key
    else:
        expiration_date = now() + timedelta(days=180)
        secret = settings.jwt_refresh_secret_key
    return jwt.encode(
        {
            'user_id': user.id,
            'exp': expiration_date,
         }, secret, algorithm='HS256')


def decode_token(token: str, is_access: bool = True):
    """
    The function will decode the security token that the client side will send
    in every request inside the header.
    :param token:
    :param is_access:
    :return: Exception or user data (dict)
    """
    if is_access:
        secret = settings.jwt_access_secret_key
    else:
        secret = settings.jwt_refresh_secret_key
    try:
        return jwt.decode(token, secret, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError('Signature has expired.')
    except Exception as ex:
        raise DecodeTokenException(f'Something is wrong with security-token. {str(ex)}')


def get_user_id_from_token(token: str) -> int:
    """
    Extract the user_id from JWT token.
    No verification is being done in this step. This ID is
    only used for a database lookup and the verification is handled separately.
    """
    try:
        data = jwt.get_unverified_claims(token)
    except Exception as ex:
        raise BadRequestException(f"Something is wrong with security-token. {str(ex)}")
    return int(data.get("user_id", 0))
