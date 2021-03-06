import uuid

import pytest


@pytest.fixture
def db_name() -> str:
    r"""Random database name for testing."""
    return f'test-{str(uuid.uuid4())}.db'
