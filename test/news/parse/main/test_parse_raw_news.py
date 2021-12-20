from datetime import datetime

import news.crawlers.db.schema
import news.parse.db.schema
import news.parse.main


def test_parse_raw_news() -> None:
    raw_news_list = [
        news.crawlers.db.schema.RawNews(
            idx=0,
            company_id=1,
            raw_xml='''
            <html>
            <head></head>
            <body>
                <div class="breadcrumb">
                    <a>首頁</a>
                    <a>新聞種類</a>
                </div>
                <div class="author">(中央社記者金城武報導)</div>
                <div class="centralContent">
                    <h1>
                        <span>新聞標題</span>
                    </h1>
                    <div class="paragraph">
                        <p>新聞內文段落一</p>
                        <p>新聞內文段落二</p>
                    </div>
                </div>
            </body>
            </html>
            ''',
            url_pattern='19951012',
        ),
        news.crawlers.db.schema.RawNews(
            idx=1,
            company_id=1,
            raw_xml='''
            <html>
            <head></head>
            <body>
                <div class="breadcrumb">
                    <a>首頁</a>
                    <a>新聞種類</a>
                </div>
                <div class="centralContent">
                    <h1>
                        <span>新聞標題</span>
                    </h1>
                    <div class="paragraph">
                        <p>(中央社記者金城武報導)</p>
                        <p>新聞內文段落一</p>
                        <p>新聞內文段落二</p>
                    </div>
                </div>
            </body>
            </html>
            ''',
            url_pattern='19951012',
        ),
    ]

    parsed_news_list = news.parse.main.parse_raw_news(
        db_path='abc',
        raw_news_list=raw_news_list,
    )

    assert len(parsed_news_list) == len(raw_news_list)

    for parsed_news, raw_news in zip(parsed_news_list, raw_news_list):
        assert isinstance(parsed_news, news.parse.db.schema.ParsedNews)
        assert isinstance(parsed_news.idx, int)
        assert parsed_news.article == '新聞內文段落一 新聞內文段落二'
        assert parsed_news.category == '新聞種類'
        assert parsed_news.company_id == raw_news.company_id
        assert parsed_news.reporter == '金城武'
        assert parsed_news.title == '新聞標題'
        assert parsed_news.timestamp == int(
            datetime(
                year=1995,
                month=10,
                day=12,
            ).timestamp()
        )
        assert parsed_news.url_pattern == raw_news.url_pattern


def test_error_msg(capsys) -> None:
    r"""Must log errors."""
    news.parse.main.parse_raw_news(
        db_path='abc',
        raw_news_list=[
            news.crawlers.db.schema.RawNews(
                idx=123,
                company_id=1,
            ),
        ],
    )

    captured = capsys.readouterr()

    # Parser will log error to stdout.
    assert 'Failed to parse idx 123 in abc:' in captured.out
