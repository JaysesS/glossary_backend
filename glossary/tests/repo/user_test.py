from unittest import TestCase
from glossary.src.core.dto.base import CreateUserDTO
from glossary.src.core.entity.base import User
from glossary.application.database.holder import db
from glossary.application.database.holder import Base
from glossary.src.data.repo.user.repo import UserRepo

db.url = "postgresql://jayse:test@localhost:5432/glossary_app_db"
db.make_engine()


class UserRepoTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        Base.metadata.create_all(bind=db._engine)
        Base.metadata.drop_all(bind=db._engine)
        Base.metadata.create_all(bind=db._engine)
        cls.session = next(db.session)
        cls.repo = UserRepo(cls.session)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.rollback()
        Base.metadata.drop_all(bind=db._engine)

    def test_save(self):
        c = CreateUserDTO(name="tuser", password="tpass")
        u = self.repo.save(c)
        self.assertIsNotNone(u.id)
        self.assertEqual(u.id, 1)
        self.assertEqual(u.name, "tuser")
        self.assertEqual(u.password, "tpass")

    def test_get(self):
        c = CreateUserDTO(name="tuser1", password="tpass1")
        u = self.repo.save(c)
        self.assertIsNotNone(u.id)
        ug = self.repo.get(id=u.id)
        self.assertEqual(u, ug)

    def test_find(self):
        c = CreateUserDTO(name="tuser2", password="tpass2")
        u = self.repo.save(c)
        self.assertIsNotNone(u.id)
        uf = self.repo.find(name="tuser2")
        self.assertEqual(u, uf)