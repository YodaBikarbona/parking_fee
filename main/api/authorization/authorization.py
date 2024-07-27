import jose
from fastapi import (
    Request,
    HTTPException, Depends,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

from main.api.logger.logger import logger
from main.api.utils.jwt_util import decode_token, get_user_id_from_token

UNAUTHORIZED = "Unauthorized"


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True, token_type: str = 'access_token'):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.token_type = token_type

    @classmethod
    def verify_token(cls, token: str, is_access: bool):
        try:
            decode_token(token=token, is_access=is_access)
        except jose.exceptions.ExpiredSignatureError as e:
            logger.error('Token expired', e)
            raise HTTPException(status_code=401, detail=UNAUTHORIZED)
        except Exception as e:
            logger.error('Token cannot be verified', e)
            raise HTTPException(status_code=401, detail=UNAUTHORIZED)

    async def __call__(self, request: Request):
        authorization: HTTPAuthorizationCredentials = await super(
            JWTBearer, self).__call__(request)
        try:
            user_id = get_user_id_from_token(authorization.credentials)
        except Exception as e:
            logger.error('Could not extract user-id from JWT token!', e)
            raise HTTPException(status_code=401, detail=UNAUTHORIZED)
        is_access_token = self.token_type == 'access_token'
        JWTBearer.verify_token(token=authorization.credentials, is_access=is_access_token)
        return {
            "user_id": user_id,
        }


class JWTRefreshBearer(JWTBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTRefreshBearer, self).__init__(auto_error=auto_error, token_type="refresh_token")


async def get_current_user_id(authorization: HTTPAuthorizationCredentials = Depends(JWTBearer())):
    # JWTBearer.__call__ returns a dict with user_id
    return authorization['user_id']
