class DomainError(Exception):

    def __init__(self, msg: str):
        self.msg = msg
        super().__init__(self.msg)

class RepoError(DomainError):
    """ """

class AuthError(DomainError):
    """"""