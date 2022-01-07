import os

import news.path


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.path, 'PROJECT_ROOT')
    assert isinstance(news.path.PROJECT_ROOT, str)
    assert os.path.isabs(news.path.PROJECT_ROOT)
    assert os.path.isdir(news.path.PROJECT_ROOT)

    assert hasattr(news.path, 'DATA_PATH')
    assert isinstance(news.path.DATA_PATH, str)
    assert os.path.isabs(news.path.DATA_PATH)
