import os
import uuid
from dataclasses import dataclass
from test.news.crawlers.conftest import MockResponse
from typing import Final, List

import pytest

import news.crawlers.db.schema
import news.crawlers.db.util


@pytest.fixture
def max_page_response(request) -> MockResponse:
    return MockResponse(
        status_code=200,
        text="""
        <html>
            <a class="page-numbers">上一頁</a>
            <a class="page-numbers">1</a>
            <a class="page-numbers">2</a>
            <a class="page-numbers">...</a>
            <a class="page-numbers">100</a>
            <a class="page-numbers">下一頁</a>
        </html>
        """,
    )
