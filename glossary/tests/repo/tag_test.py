from unittest import TestCase
from glossary.src.core.dto.base import CreateTagDTO
from glossary.application.database.holder import db
from glossary.application.database.holder import Base
from glossary.src.data.repo.tag.repo import TagRepo

db.url = "postgresql://jayse:test@localhost:5432/glossary_app_db"
db.make_engine()


class TagRepoTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        Base.metadata.create_all(bind=db._engine)
        Base.metadata.drop_all(bind=db._engine)
        Base.metadata.create_all(bind=db._engine)
        cls.session = next(db.session)
        cls.repo = TagRepo(cls.session)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.rollback()
        Base.metadata.drop_all(bind=db._engine)

    def test_save(self):
        ct = CreateTagDTO(
            name="super_tag",
            description="**desc**",
        )
        tag = self.repo.save(ct)
        self.assertIsNotNone(tag.id)
        self.assertEqual(tag.name, "super_tag")
        self.assertEqual(tag.description, "**desc**")
