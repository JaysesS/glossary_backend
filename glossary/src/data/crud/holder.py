from glossary.src.data.crud.base import CRUDASyncBase
from glossary.src.data.models import UserModel, TagModel, WordModel, WordTagModel
from glossary.src.core.schemas.entity import (
    UserSchema, UserCreateSchema, UserUpdateSchema,
    TagSchema, TagCreateSchema, TagUpdateSchema,
    WordSchema, WordCreateSchema, WordUpdateSchema
)

class UserCRUD(CRUDASyncBase[UserModel, UserCreateSchema, UserUpdateSchema]):
    """ Declare model specific CRUD operation methods. """

user_crud = UserCRUD(UserModel)

class TagCRUD(CRUDASyncBase[TagModel, TagCreateSchema, TagUpdateSchema]):
    """ Declare model specific CRUD operation methods. """

tag_crud = TagCRUD(TagModel)

class WordCRUD(CRUDASyncBase[WordModel, WordCreateSchema, WordUpdateSchema]):
    """ Declare model specific CRUD operation methods. """

word_crud = WordCRUD(WordModel)