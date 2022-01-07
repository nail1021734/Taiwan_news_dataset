import pytest

import news.crawlers.util.status_code


def test_got_banned() -> None:
    r"""Must raise exception when crawlers got banned."""
    with pytest.raises(Exception) as exc_info:
        news.crawlers.util.status_code.check_status_code(
            company_id=0,
            status_code=403,
            url='http://example.com',
        )

    assert 'Got banned.' in str(exc_info.value)


def test_not_found() -> None:
    r"""Must raise exception when URL not found."""
    with pytest.raises(Exception) as exc_info:
        news.crawlers.util.status_code.check_status_code(
            company_id=0,
            status_code=404,
            url='http://example.com',
        )

    assert 'URL not found.' in str(exc_info.value)


def test_too_many_request() -> None:
    r"""Must raise exception when too many request."""
    with pytest.raises(Exception) as exc_info:
        news.crawlers.util.status_code.check_status_code(
            company_id=1,
            status_code=429,
            url='http://example.com',
        )

    assert 'Too many requests.' in str(exc_info.value)


def test_not_normal() -> None:
    r"""Must raise exception when status code is not 200."""
    for status_code in [500, 418]:
        with pytest.raises(Exception) as exc_info:
            news.crawlers.util.status_code.check_status_code(
                company_id=1,
                status_code=status_code,
                url='http://example.com',
            )

        assert 'http://example.com is weird.' in str(exc_info.value)


def test_200() -> None:
    r"""Nothing happen when status code is 200."""
    news.crawlers.util.status_code.check_status_code(
        company_id=0,
        status_code=200,
        url='http://example.com',
    )
