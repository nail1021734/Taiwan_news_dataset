from datetime import datetime, timezone

import news.crawlers.udn


def test_get_last_available_page() -> None:
    r"""Must have more than one page."""
    last_ava_page = news.crawlers.udn.get_last_available_page(
        past_datetime=datetime.now(tz=timezone.utc),
    )
    assert last_ava_page > 1
