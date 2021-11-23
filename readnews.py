import sys
import news.parse.db.read as Newsread

if __name__ == '__main__':
    news = Newsread.read_all_records(sys.argv[1])
    for new in news[850:]:
        print(new.pretify())
        input()