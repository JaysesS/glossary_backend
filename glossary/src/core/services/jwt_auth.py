import jwt
from datetime import datetime, timedelta
from glossary.src.core.exception.base import AuthError
from glossary.src.core.interfaces.services.iauth import IAuthService

class AuthJWTService(IAuthService):

    secret: str
    lifetime: int

    def generate_token(self, user_id: int) -> str:
        expires_in =  int(
            (datetime.now() + timedelta(seconds=self.lifetime)
        ).timestamp())
        payload = {"user_id": user_id, "exp": expires_in}
        token = jwt.encode(payload, self.secret, algorithm="HS256")
        return token
    
    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthError("Token expired")
        except Exception:
            raise AuthError("Fail on verify token signature")
        return payload

    def configure(self, secret: str, lifetime: int):
        self.secret = secret
        self.lifetime = lifetime

auth_service = AuthJWTService()
