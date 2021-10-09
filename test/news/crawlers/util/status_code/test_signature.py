import inspect
from inspect import Parameter, Signature
from typing import Final, Optional

import news.crawlers.util.status_code


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.util.status_code, 'gen_non_neg')
    assert inspect.isfunction(news.crawlers.util.status_code.gen_non_neg)
    assert (
        inspect.signature(news.crawlers.util.status_code.gen_non_neg)
        ==
        Signature(
            parameters=[
                Parameter(
                    name='mu',
                    kind=Parameter.KEYWORD_ONLY,
                    default=1.0,
                    annotation=Final[Optional[float]],
                ),
                Parameter(
                    name='sigma',
                    kind=Parameter.KEYWORD_ONLY,
                    default=2.0,
                    annotation=Final[Optional[float]],
                ),
                Parameter(
                    name='upper_bound',
                    kind=Parameter.KEYWORD_ONLY,
                    default=10.0,
                    annotation=Final[Optional[float]],
                ),
            ],
            return_annotation=float,
        )
    )
    assert hasattr(news.crawlers.util.status_code, 'sleep_after_banned')
    assert inspect.isfunction(
        news.crawlers.util.status_code.sleep_after_banned,
    )
    assert (
        inspect.signature(news.crawlers.util.status_code.sleep_after_banned)
        ==
        Signature(
            parameters=[
                Parameter(
                    name='company_id',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[int],
                ),
            ],
            return_annotation=None,
        )
    )
    assert hasattr(news.crawlers.util.status_code, 'sleep_after_429')
    assert inspect.isfunction(
        news.crawlers.util.status_code.sleep_after_429,
    )
    assert (
        inspect.signature(news.crawlers.util.status_code.sleep_after_429)
        ==
        Signature(
            parameters=[
                Parameter(
                    name='company_id',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[int],
                ),
            ],
            return_annotation=None,
        )
    )
    assert hasattr(news.crawlers.util.status_code, 'sleep_before_banned')
    assert inspect.isfunction(
        news.crawlers.util.status_code.sleep_before_banned,
    )
    assert (
        inspect.signature(news.crawlers.util.status_code.sleep_before_banned)
        ==
        Signature(
            parameters=[
                Parameter(
                    name='company_id',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[int],
                ),
            ],
            return_annotation=None,
        )
    )
    assert hasattr(news.crawlers.util.status_code, 'check_status_code')
    assert inspect.isfunction(
        news.crawlers.util.status_code.check_status_code,
    )
    assert (
        inspect.signature(news.crawlers.util.status_code.check_status_code)
        ==
        Signature(
            parameters=[
                Parameter(
                    name='company_id',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[int],
                ),
                Parameter(
                    name='status_code',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[int],
                ),
                Parameter(
                    name='url',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[str],
                ),
            ],
            return_annotation=None,
        )
    )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(
        news.crawlers.util.status_code,
        'SLEEP_SECS_BEFORE_BANNED_LOOKUP_TABLE',
    )
    assert (
        news.crawlers.util.status_code.SLEEP_SECS_BEFORE_BANNED_LOOKUP_TABLE
        ==
        {
            0: 0.0,
            1: 0.0,
            2: 0.0,
            3: 0.0,
            4: 0.0,
            5: 60.0,
            6: 0.0,
            7: 60.0,
            8: 1.0,
            9: 0.0,
            10: 0.0,
        }
    )
    assert hasattr(
        news.crawlers.util.status_code,
        'SLEEP_SECS_BEFORE_BANNED_FASTEST_LOOKUP_TABLE',
    )
    assert (
        (
            news.crawlers.util.status_code
            .SLEEP_SECS_BEFORE_BANNED_FASTEST_LOOKUP_TABLE
        )
        ==
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            60.0,
            0.0,
            60.0,
            1.0,
            0.0,
            0.0,
        ]
    )
    assert hasattr(
        news.crawlers.util.status_code,
        'SLEEP_SECS_AFTER_BANNED_LOOKUP_TABLE',
    )
    assert (
        news.crawlers.util.status_code.SLEEP_SECS_AFTER_BANNED_LOOKUP_TABLE
        ==
        {
            0: 0.0,
            1: 0.0,
            2: 0.0,
            3: 0.0,
            4: 0.0,
            5: 86400.0,
            6: 0.0,
            7: 86400.0,
            8: 0.0,
            9: 0.0,
            10: 86400.0,
        }
    )
    assert hasattr(
        news.crawlers.util.status_code,
        'SLEEP_SECS_AFTER_BANNED_FASTEST_LOOKUP_TABLE',
    )
    assert (
        (
            news.crawlers.util.status_code
            .SLEEP_SECS_AFTER_BANNED_FASTEST_LOOKUP_TABLE
        )
        ==
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            86400.0,
            0.0,
            86400.0,
            0.0,
            0.0,
            86400.0,
        ]
    )
    assert hasattr(
        news.crawlers.util.status_code,
        'SLEEP_SECS_AFTER_429_LOOKUP_TABLE',
    )
    assert (
        news.crawlers.util.status_code.SLEEP_SECS_AFTER_429_LOOKUP_TABLE
        ==
        {
            0: 120.0,
            1: 0.0,
            2: 120.0,
            3: 0.0,
            4: 0.0,
            5: 120.0,
            6: 120.0,
            7: 120.0,
            8: 0.0,
            9: 0.0,
            10: 120.0,
        }
    )
    assert hasattr(
        news.crawlers.util.status_code,
        'SLEEP_SECS_AFTER_429_FASTEST_LOOKUP_TABLE',
    )
    assert (
        (
            news.crawlers.util.status_code
            .SLEEP_SECS_AFTER_429_FASTEST_LOOKUP_TABLE
        )
        ==
        [
            120.0,
            0.0,
            120.0,
            0.0,
            0.0,
            120.0,
            120.0,
            120.0,
            0.0,
            0.0,
            120.0,
        ]
    )
