from datetime import datetime, timedelta, timezone

import news.crawlers.udn


def test_get_last_vaild_page() -> None:
    r"""Must have more than 1 valid page."""
    last_valid_page = news.crawlers.udn.get_last_vaild_page(
        last_ava_page=3000,
        past_datetime=datetime.now(tz=timezone.utc) - timedelta(days=2),
    )
    assert last_valid_page > 1
