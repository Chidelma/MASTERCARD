import sys
from pathlib import Path
from collections.abc import Generator

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from python_api.db.schemas import Base
from tests.consts import engine


@pytest.fixture(autouse=True)
def setup_db() -> Generator[None, None, None]:
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
