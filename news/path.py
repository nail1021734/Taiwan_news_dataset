import os
from typing import Final

# 專案根目錄路徑
PROJECT_ROOT: Final[str] = os.path.abspath(os.path.join(
    os.path.abspath(__file__),
    os.pardir,
    os.pardir,
))
