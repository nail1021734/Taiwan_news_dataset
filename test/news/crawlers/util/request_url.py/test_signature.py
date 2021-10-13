import inspect
from inspect import Parameter, Signature
from typing import Final, Optional

import requests

import news.crawlers.util.request_url


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.util.request_url, 'get')
    assert inspect.isfunction(news.crawlers.util.request_url.get)
    assert inspect.signature(news.crawlers.util.request_url.get) \
        == Signature(
            parameters=[
                Parameter(
                    name='url',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[str],
                ),
                Parameter(
                    name='timeout',
                    kind=Parameter.KEYWORD_ONLY,
                    default=20.0,
                    annotation=Final[Optional[float]],
                ),
            ],
            return_annotation=requests.Response,
        )
