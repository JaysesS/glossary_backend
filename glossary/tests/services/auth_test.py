from unittest import TestCase
from glossary.tests.deps import settings

from glossary.src.core.exception.base import AuthError
from glossary.src.core.services.jwt_auth import AuthJWTService

RND_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2NTY3MTI1MDV9.rfQVhj5-4C0FSpWW2oZeauERW_dstZfMAt2_nai74fs"


class AuthServiceTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.auth_service = AuthJWTService()
        cls.auth_service.configure(
            secret=settings.SECRET_KEY,
            lifetime=settings.TOKEN_LIFE_TIME
        )

    def test_configure(self):
        self.assertEqual(
            self.auth_service.secret, settings.SECRET_KEY
        )
        self.assertEqual(
            self.auth_service.lifetime, settings.TOKEN_LIFE_TIME
        )
    
    def test_generate_token(self):
        user_id = 1337
        token = self.auth_service.generate_token(
            user_id=user_id
        )
        self.assertNotEqual(token, user_id)
        payload = self.auth_service.verify_token(
            token=token
        )
        self.assertEqual(
            payload["user_id"], user_id
        )

    def test_not_verify(self):
        with self.assertRaises(expected_exception=AuthError):
            self.auth_service.verify_token(
                token=RND_TOKEN
            )
