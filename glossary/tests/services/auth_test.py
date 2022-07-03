from unittest import TestCase
from glossary.src.core.dto.base import CreateUserDTO
from glossary.application.database.holder import db
from glossary.application.database.holder import Base
from glossary.src.core.services.jwt_auth import AuthJWTService
from glossary.src.data.repo.sql_repo.repo import GlossarySQLRepo

db.url = "postgresql://jayse:test@localhost:5432/glossary_app_db"
db.make_engine()

SECRET = "notsecret"
OLD_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2NTY3MTI1MDV9.rfQVhj5-4C0FSpWW2oZeauERW_dstZfMAt2_nai74fs"


class AuthServiceTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        Base.metadata.create_all(bind=db._engine)
        Base.metadata.drop_all(bind=db._engine)
        Base.metadata.create_all(bind=db._engine)
        cls.session = next(db.session)
        cls.repo = GlossarySQLRepo(cls.session)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.rollback()
        Base.metadata.drop_all(bind=db._engine)

    def test_login(self):
        auth_service = AuthJWTService(secret=SECRET, lifetime=50)
        c = CreateUserDTO(name="tuser", password="tpass")
        u = self.repo.save_user(c)
        self.assertIsNotNone(u.id)

        token = auth_service.login(name="tuser", password="tpass", repo=self.repo)
        self.assertIsInstance(token, str)
        user_id = auth_service.get_user_id(token=token)
        self.assertEqual(user_id, u.id)

    def test_check(self):
        auth_service = AuthJWTService(secret=SECRET, lifetime=50)
        c = CreateUserDTO(name="tuser1", password="tpass1")
        u = self.repo.save_user(c)
        self.assertIsNotNone(u.id)

        token = auth_service.login(name="tuser1", password="tpass1", repo=self.repo)
        assrt = auth_service.check(token=token, repo=self.repo)
        self.assertTrue(assrt)
