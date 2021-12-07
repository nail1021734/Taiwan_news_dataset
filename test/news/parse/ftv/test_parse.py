import glob
import json
import os
import re
from functools import partial
from operator import itemgetter
from typing import List

import pytest

import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.ftv
from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews
from news.utils.dataclass_serialize import (
    dataclass_from_dict, dataclass_to_json
)


def xml_from_web(url_pattern):
    url = f'https://www.ftvnews.com.tw/news/detail/{url_pattern}'
    response = news.crawlers.util.request_url.get(url=url)
    return news.crawlers.util.normalize.compress_raw_xml(raw_xml=response.text)


def xml_from_local(localhost, url_pattern):
    """
    fetch compressed raw xml from local server
    """
    url = localhost + url_pattern
    response = news.crawlers.util.request_url.get(url=url)
    return response.text


@pytest.fixture()
def get_xml(request):
    local = request.config.getoption("--local")
    return xml_from_web if len(local) == 0 else partial(xml_from_local, local)


def serialize_tests_to_json(tests: List[RawNews]) -> str:
    """
    Serialize list of RarsedNews to json format
    """
    return dataclass_to_json(tests)


def get_tests_from_json(testname: str) -> List[ParsedNews]:
    """
    Read expected answer from json which contains list of serialized RarsedNews
    """
    p = os.path.join(os.path.dirname(__file__), testname)
    parsed_from_dict = lambda x: dataclass_from_dict(ParsedNews, x)
    return list(map(parsed_from_dict, json.load(open(p))))


def test_pattern(get_xml, testname) -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='民視')
    tests = get_tests_from_json(testname)
    for expected in tests:
        raw_news = RawNews(
            company_id=company_id,
            raw_xml=get_xml(expected.url_pattern),
            url_pattern=expected.url_pattern
        )
        parsed_news = news.parse.ftv.parser(raw_news=raw_news)

        assert parsed_news.article == expected.article
        assert parsed_news.category == expected.category
        assert parsed_news.company_id == expected.company_id
        assert parsed_news.reporter == expected.reporter
        assert parsed_news.timestamp == expected.timestamp
        assert parsed_news.title == expected.title
        assert parsed_news.url_pattern == expected.url_pattern


def pytest_generate_tests(metafunc):

    def gen_tests():
        for pipeline in ['reporter', 'article']:
            tests = glob.glob(
                os.path.join(
                    os.path.dirname(__file__),
                    f'testcases/{pipeline}/*.json',
                )
            )
            tests = [
                (int(re.match(r'.+/(-?\d+)\.json', i).group(1)), i)
                for i in tests
            ]
            for i, t in enumerate(map(itemgetter(1), sorted(tests))):
                yield t, f'{pipeline}_{i}'

    tc, ids = zip(*gen_tests())
    metafunc.parametrize('testname', tc, ids=ids)
