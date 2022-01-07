import news.crawlers.ftv


def test_page_found() -> None:
    r"""Must return `False` when page is found."""
    assert not news.crawlers.ftv.page_not_found(raw_xml='')


def test_page_not_found() -> None:
    r"""Must return `True` when page not found."""
    assert news.crawlers.ftv.page_not_found(
        raw_xml="""
            <script language="javascript">alert('資料不存在!');</script>
            <noscript>
                抱歉您的瀏覽器不支援Javascript或VBscript，
                請使用IE6.0或Netscape7.1以上瀏覽~請按ALT+F4離開視窗
            </noscript>
            <script language="javascript">location.href='/404';</script>
            <noscript>
                抱歉您的瀏覽器不支援Javascript或VBscript，
                請使用IE6.0或Netscape7.1以上瀏覽~請按ALT+F4離開視窗
            </noscript>
        """,
    )
