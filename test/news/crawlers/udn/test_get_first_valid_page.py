from datetime import datetime, timedelta, timezone

import news.crawlers.udn


def test_get_first_vaild_page() -> None:
    r"""Must have more than 1 valid page."""
    first_valid_page = news.crawlers.udn.get_first_vaild_page(
        last_valid_page=1000,
        current_datetime=datetime.now(tz=timezone.utc) - timedelta(days=2),
    )
    assert first_valid_page > 1
