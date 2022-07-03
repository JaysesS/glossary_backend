import jwt
from datetime import datetime, timedelta
from glossary.src.core.entity.base import User
from glossary.src.core.exception.base import AuthError
from glossary.application.settings import get_settings
from glossary.src.core.interfaces.repo.iglossary_sql_repo import IGlossarySQLRepo
from glossary.src.core.interfaces.services.iauth import IAuthService

class AuthJWTService(IAuthService):

    def __init__(self, secret: str, lifetime: int) -> None:
        self.secret = secret
        self.lifetime = lifetime

    def _generate_token(self, user_id: int) -> str:
        expires_in =  int(
            (datetime.now() + timedelta(seconds=self.lifetime)
        ).timestamp())
        payload = {"user_id": user_id, "exp": expires_in}
        token = jwt.encode(payload, self.secret, algorithm="HS256")
        return token
    
    def _verify_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthError("Token expired")
        except Exception:
            raise AuthError("Fail on verify token signature")
        user_id = payload["user_id"]
        return user_id

    def login(self, name: str, password: str, repo: IGlossarySQLRepo) -> str:
        user = repo.find_user(name=name)
        if not user:
            raise AuthError("Credential error")
        if user.password != password:
            raise AuthError("Credential error")
        token = self._generate_token(user_id=user.id)
        return token

    def get_user_id(self, token: str) -> int:
        return self._verify_token(token=token)
    
    def check(self, token: str, repo: IGlossarySQLRepo) -> User:
        user_id = self._verify_token(token=token)
        user = repo.get_user(user_id)
        if not user:
            raise AuthError("Payload fail")
        return user

settings = get_settings()

auth_service = AuthJWTService(
    secret=settings.SECRET_KEY,
    lifetime=settings.TOKEN_LIFE_TIME
)
