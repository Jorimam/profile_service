from ..database import get_db
from fastapi import Depends, Request, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime
from ..auth.jwt import verify_access_token
# from ..models.user import User
from ..models.users import User
import logging




# HTTPBearer is responsible forextracting Bearer token from authorization headers

security = HTTPBearer()


# http exception
def raiseHttpException(e, status_code=status.HTTP_403_FORBIDDEN):
       raise HTTPException(
                status_code=status_code,
                detail = {
                    'msg':e,
                    'timestamp':f"{datetime.utcnow()}"
                }
            )




class JWTBearer(HTTPBearer):
    def __init__(self, auto_error:bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request, db: Session = Depends(get_db)):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials:
            if credentials.scheme != 'Bearer':
                raiseHttpException("invalid authorization schem. expected \'Bearer\'")

            # verify token and get payload
            verified_user = self.verify_jwt(credentials.credentials, db)
            if not verified_user:
                raiseHttpException('usr no found')
            return verified_user

        else:
            raiseHttpException("invalid authorization code")

    def verify_jwt(self, token: str, db: Session = Depends(get_db)):
        try:
            payload = verify_access_token(token)
            user_id = payload.get('sub')

            if user_id is None:
                return False

            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                raiseHttpException("user does not exist")

            return user
        except Exception as e:
            raiseHttpException(f"JWT verification failed: {e}")

AuthMiddleware = JWTBearer()