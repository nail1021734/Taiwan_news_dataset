import os

# 專案根目錄路徑
PROJECT_ROOT: str = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        os.pardir,
        os.pardir,
    )
)

# 資料集存放目錄
DATA_PATH: str = os.path.join(PROJECT_ROOT, 'data')
