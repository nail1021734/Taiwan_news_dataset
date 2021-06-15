import sqlite3

import torch


class Seq2SeqNewsDataset(torch.utils.data.Dataset):
    r"""
    Dataset for seq2seq models.
    return a tuple contain title and article as below format

    return: (title, article)
    """

    def __init__(self, db_path: str):
        super().__init__()

        # Connect to DB.
        conn = sqlite3.connect(db_path)

        # Set `conn.row_factory` to get right return format.
        conn.row_factory = lambda cursor, row: row[0]

        # Get database cursor.
        cursor = conn.cursor()

        # Get all news title and article.
        self.titles = list(cursor.execute('SELECT title from news_table;'))
        self.articles = list(cursor.execute('SELECT article from news_table;'))

    def __getitem__(self, index: int):
        return self.titles[index], self.articles[index]

    def __len__(self):
        return len(self.titles)


class LMNewsDataset(torch.utils.data.Dataset):
    r"""
    Dataset for languange models.
    return a string contain title and article as below format

    return: [SEP] + title + [SEP] + article + [SEP]
    """

    def __init__(self, db_path: str):
        super().__init__()

        # Connect to DB.
        conn = sqlite3.connect(db_path)

        # Set `conn.row_factory` to get right return format.
        conn.row_factory = lambda cursor, row: row[0]

        # Get database cursor.
        cursor = conn.cursor()

        # Get all news title and article.
        self.titles = list(cursor.execute('SELECT title from news_table;'))
        self.articles = list(cursor.execute('SELECT article from news_table;'))

        # Merge title and article into single string.
        self.merge_data = [
            f'[SEP]{self.titles[i]}[SEP]{self.articles[i]}[SEP]' for i in range(len(self.titles))]

    def __getitem__(self, index: int):
        return self.merge_data[index]

    def __len__(self):
        return len(self.titles)

class Allcolumn(torch.utils.data.Dataset):
    def __init__(self, db_path: str):
        super().__init__()

        # Connect to DB.
        conn = sqlite3.connect(db_path)

        # Set `conn.row_factory` to get right return format.
        conn.row_factory = lambda cursor, row: row[0]

        # Get database cursor.
        cursor = conn.cursor()

        # Get all news title and article.
        self.ids = list(cursor.execute('SELECT id from news_table;'))
        self.urls = list(cursor.execute('SELECT url from news_table;'))
        self.times = list(cursor.execute('SELECT time from news_table;'))
        self.companys = list(cursor.execute('SELECT company from news_table;'))
        self.labels = list(cursor.execute('SELECT label from news_table;'))
        self.reporters = list(cursor.execute('SELECT reporter from news_table;'))
        self.titles = list(cursor.execute('SELECT title from news_table;'))
        self.articles = list(cursor.execute('SELECT article from news_table;'))


    def __getitem__(self, index: int):
        return {
            'id': self.ids[index],
            'url': self.urls[index],
            'time': self.times[index],
            'company': self.companys[index],
            'label': self.labels[index],
            'reporter': self.reporters[index],
            'title': self.titles[index],
            'article': self.articles[index],
        }

    def __len__(self):
        return len(self.titles)


if __name__ == "__main__":
    # Initial example.
    dataset = Allcolumn(db_path='news.db')
