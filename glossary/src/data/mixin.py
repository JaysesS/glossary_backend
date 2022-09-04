from sqlalchemy import Column, DateTime
from sqlalchemy import func

class TimeMixin(object):
    created_at = created_at = Column(
        DateTime(timezone=True),
        nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now()
    )