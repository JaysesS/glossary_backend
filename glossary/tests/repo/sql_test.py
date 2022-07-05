from unittest import TestCase
from uuid import uuid4
from glossary.application.database.holder import db
from glossary.application.database.holder import Base
from glossary.src.data.glossary_repo.sql_repo.repo import GlossarySQLRepo
from glossary.src.core.dto.base import CreatePriorityDTO, CreateTagDTO, CreateUserDTO, CreateWordDTO, UpdateTagDTO, UpdateWordDTO
from glossary.src.data.user_repo.sql_repo.repo import UserSQLRepo

db.url = "postgresql://jayse:test@localhost:5432/glossary_app_db"
db.make_engine()


class GlossarySQLRepoTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        Base.metadata.create_all(bind=db._engine)
        Base.metadata.drop_all(bind=db._engine)
        Base.metadata.create_all(bind=db._engine)
        cls.session = next(db.session)
        cls.repo = GlossarySQLRepo(cls.session)
        cls.user_repo = UserSQLRepo(cls.session)

        cp = CreatePriorityDTO(name="low")
        cls.priority = cls.repo.save_priority(cp)
        cp2 = CreatePriorityDTO(name="high")
        cls.priority2 = cls.repo.save_priority(cp2)

    # @classmethod
    # def tearDownClass(cls) -> None:
    #     cls.session.rollback()
    #     Base.metadata.drop_all(bind=db._engine)

    def test_save_user(self):
        name = str(uuid4())
        c = CreateUserDTO(name=name, password="tpass")
        u = self.user_repo.save_user(c)
        self.assertIsNotNone(u.id)
        self.assertIsNotNone(u.id)
        self.assertEqual(u.name, name)
        self.assertEqual(u.password, "tpass")

    def test_get_user(self):
        c = CreateUserDTO(name=str(uuid4()), password="tpass1")
        u = self.user_repo.save_user(c)
        self.assertIsNotNone(u.id)
        ug = self.user_repo.get_user(id=u.id)
        self.assertEqual(u, ug)

    def test_find_user(self):
        name = str(uuid4())
        c = CreateUserDTO(name=name, password="tpass2")
        u = self.user_repo.save_user(c)
        self.assertIsNotNone(u.id)
        uf = self.user_repo.find_user(name=name)
        self.assertEqual(u, uf)

    def test_list_tag(self):
        c = CreateUserDTO(name=str(uuid4()), password="tpass")
        u = self.user_repo.save_user(c)
        ct = CreateTagDTO(
            name="super_tag2",
            description="**desc 2**",
        )
        self.repo.save_tag(ct, user_id=u.id)
        ct = CreateTagDTO(
            name="super_tag3",
            description="**desc 3**",
        )
        tag = self.repo.save_tag(ct, user_id=u.id)

        tl = self.repo.list_tag(user_id=u.id)
        self.assertTrue(len(tl) > 0)

        tl = self.repo.list_tag(ids=[tag.id], user_id=u.id)
        self.assertTrue(len(tl) == 1)

        tl = self.repo.list_tag(limit=1, user_id=u.id)
        self.assertTrue(len(tl) == 1)

    def test_rm_tag(self):
        c = CreateUserDTO(name=str(uuid4()), password="tpass")
        u = self.user_repo.save_user(c)
        ct = CreateTagDTO(
            name="super_tag5",
            description="**desc 5**",
        )
        tag = self.repo.save_tag(ct, user_id=u.id)
        tag_count = len(self.repo.list_tag(user_id=u.id))
        rm_id = self.repo.rm_tag(id=tag.id, user_id=u.id)
        self.assertEqual(rm_id, tag.id)
        self.assertTrue(tag_count - 1 == len(self.repo.list_tag(user_id=u.id)))

    def test_get_tag(self):
        c = CreateUserDTO(name=str(uuid4()), password="tpass")
        u = self.user_repo.save_user(c)
        ct = CreateTagDTO(
            name="super_tag6",
            description="**desc 6**",
        )
        tag = self.repo.save_tag(ct, user_id=u.id)
        tg = self.repo.get_tag(tag.id, user_id=u.id)
        self.assertEqual(tag.id, tg.id) # type: ignore
        self.assertEqual(tag.name, tg.name) # type: ignore
        self.assertEqual(tag.description, tg.description)  # type: ignore

    def test_update_tag(self):
        c = CreateUserDTO(name=str(uuid4()), password="tpass")
        u = self.user_repo.save_user(c)
        ct = CreateTagDTO(
            name="super_tag6",
            description="**desc 6**",
        )
        tag = self.repo.save_tag(ct, user_id=u.id)
        tag_upd_dto = UpdateTagDTO(
            id=tag.id,
            name="TEST_UPD_NAME",
            description="TEST_UPD_DESC"
        )
        tag_upd = self.repo.update_tag(tag=tag_upd_dto, user_id=u.id)
        self.assertEqual(tag_upd.name, "TEST_UPD_NAME")
        self.assertEqual(tag_upd.description, "TEST_UPD_DESC")

    def test_update_word(self):
        c = CreateUserDTO(name=str(uuid4()), password="tpass")
        u = self.user_repo.save_user(c)
        ct = CreateTagDTO(
            name="super_tag6",
            description="**desc 6**",
        )
        tag = self.repo.save_tag(ct, user_id=u.id)
        ct = CreateTagDTO(
            name="super_tag7",
            description="**desc 7**",
        )
        tag2 = self.repo.save_tag(ct, user_id=u.id)

        cw = CreateWordDTO(
            name="super_word",
            description="**desc**",
            tag_ids=[tag.id],
            priority_id=self.priority.id,
        )
        word = self.repo.save_word(cw, user_id=u.id)
        tag_ids_cur = [tag.id for tag in word.tags]
        word_upd_tag = UpdateWordDTO(
            id=word.id,
            name="TEST_UPDATE_NAME",
            description="TEST_UPDATE_DESK",
            priority_id=self.priority2.id,
            tag_ids=[tag2.id]
        )
        upd_word = self.repo.update_word(
            word = word_upd_tag, user_id=u.id
        )
        tag_ids_upd = [tag.id for tag in upd_word.tags]
        self.assertEqual(upd_word.name, "TEST_UPDATE_NAME")
        self.assertEqual(upd_word.description, "TEST_UPDATE_DESK")
        self.assertEqual(upd_word.priority, self.priority2)
        self.assertEqual(tag_ids_upd, [tag2.id])


    def test_save_word(self):
        c = CreateUserDTO(name=str(uuid4()), password="tpass")
        u = self.user_repo.save_user(c)
        ct = CreateTagDTO(
            name="super_tag6",
            description="**desc 6**",
        )
        tag = self.repo.save_tag(ct, user_id=u.id)

        cw = CreateWordDTO(
            name="super_word",
            description="**desc**",
            tag_ids=[tag.id],
            priority_id=self.priority.id,
        )
        self.repo.save_word(cw, user_id=u.id)

        cw = CreateWordDTO(
            name="super_word2",
            description="**desc**",
            tag_ids=[],
            priority_id=self.priority.id,
        )
        self.repo.save_word(cw, user_id=u.id)

    def test_list_word(self):
        c = CreateUserDTO(name=str(uuid4()), password="tpass")
        u = self.user_repo.save_user(c)
        ct = CreateTagDTO(
            name="super_tag6",
            description="**desc 6**",
        )
        tag = self.repo.save_tag(ct, user_id=u.id)

        cw = CreateWordDTO(
            name="super_word3",
            description="**desc3**",
            tag_ids=[tag.id],
            priority_id=self.priority.id,
        )
        self.repo.save_word(cw, user_id=u.id)

        cw = CreateWordDTO(
            name="super_word4",
            description="**desc4**",
            tag_ids=[],
            priority_id=self.priority.id,
        )
        self.repo.save_word(cw, user_id=u.id)

        rw = self.repo.list_word(user_id=u.id)
        self.assertTrue(len(rw) > 0)
        
        rw = self.repo.list_word(tag_ids=[tag.id],user_id=u.id)
        self.assertTrue(len(rw) > 0)
        
        rw = self.repo.list_word(limit=1, user_id=u.id)
        self.assertTrue(len(rw) == 1)

    def test_rm_word(self):
        c = CreateUserDTO(name=str(uuid4()), password="tpass")
        u = self.user_repo.save_user(c)
        ct = CreateTagDTO(
            name="super_tag6",
            description="**desc 6**",
        )
        tag = self.repo.save_tag(ct, user_id=u.id)

        cw = CreateWordDTO(
            name="super_word3",
            description="**desc3**",
            tag_ids=[tag.id],
            priority_id=self.priority.id,
        )
        word = self.repo.save_word(cw, user_id=u.id)
        word_count = len(self.repo.list_word(user_id=u.id))
        self.assertTrue(word_count > 0)

        rm_id = self.repo.rm_word(id=word.id, user_id=u.id)
        self.assertIsInstance(rm_id, int)

