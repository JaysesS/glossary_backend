class DomainError(Exception):

    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(self.msg)

class CrudError(DomainError):
    """ """

class CrudNotFoundError(CrudError):
    """ """

class AuthError(DomainError):
    """"""