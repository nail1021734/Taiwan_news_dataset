import os
import uuid
from dataclasses import dataclass
from typing import Final, List

import pytest

import news.crawlers.db.schema
import news.crawlers.db.util


@pytest.fixture
def cleanup_db_file(db_name: Final[str], request: Final) -> None:
    r"""Delete testing database files."""

    def remove() -> None:
        db_path = news.crawlers.db.util.get_db_path(db_name=db_name)
        db_dir = os.path.abspath(os.path.join(db_path, os.pardir))

        if os.path.exists(db_path):
            os.remove(db_path)

        if os.path.exists(db_dir) and not os.listdir(db_dir):
            os.removedirs(db_dir)

    request.addfinalizer(remove)


@dataclass
class MockResponse:
    status_code: int
    text: str

    def close(self) -> None:
        pass


@pytest.fixture
def response_200(request) -> MockResponse:
    return MockResponse(status_code=200, text=str(uuid.uuid4()))


@pytest.fixture
def response_403() -> MockResponse:
    return MockResponse(status_code=403, text=str(uuid.uuid4()))


@pytest.fixture
def response_404() -> MockResponse:
    return MockResponse(status_code=404, text=str(uuid.uuid4()))


@pytest.fixture
def response_410() -> MockResponse:
    return MockResponse(status_code=410, text=str(uuid.uuid4()))


@pytest.fixture
def response_429() -> MockResponse:
    return MockResponse(status_code=429, text=str(uuid.uuid4()))


@pytest.fixture
def response_500() -> MockResponse:
    return MockResponse(status_code=500, text=str(uuid.uuid4()))


@pytest.fixture
def all_responses(
    response_200: Final[MockResponse],
    response_403: Final[MockResponse],
    response_404: Final[MockResponse],
    response_410: Final[MockResponse],
    response_429: Final[MockResponse],
    response_500: Final[MockResponse],
) -> List[MockResponse]:
    return [
        response_200,
        response_403,
        response_404,
        response_410,
        response_429,
        response_500,
    ]
