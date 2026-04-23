from collections.abc import Generator

import pytest

from python_api.db.schemas import Base
from tests.consts import engine


@pytest.fixture(autouse=True)
def setup_db() -> Generator[None, None, None]:
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
