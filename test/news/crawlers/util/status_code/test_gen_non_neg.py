from collections import Counter

import news.crawlers.util.status_code


def test_randomness() -> None:
    r"""Ensure random generation."""
    counter = Counter([
        news.crawlers.util.status_code.gen_non_neg()
        for i in range(100)
    ])

    assert len(set(counter.keys())) >= 2


def test_non_negative() -> None:
    r"""Must generate non-negative numbers."""
    for i in range(100):
        assert news.crawlers.util.status_code.gen_non_neg() > 0.0


def test_upper_bound() -> None:
    r"""Must generate numbers smaller than upper bound."""
    upper_bound = 5.0
    for i in range(100):
        assert (
            news.crawlers.util.status_code.gen_non_neg(upper_bound=upper_bound)
            <=
            upper_bound
        )
