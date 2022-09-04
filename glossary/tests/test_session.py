import pytest
from glossary.tests.deps import db

# pytest glossary/tests/test_session.py

# pytest glossary/tests/test_session.py::test_get_session -s
@pytest.mark.asyncio
async def test_get_session():
    async with db.session() as session:  # type: ignore
        r = await session.execute("select 1")
        av, = r.one()
        assert 1 == av