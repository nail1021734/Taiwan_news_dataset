import news.parse.db.read

d = news.parse.db.read.read_all_records('1_1000.db')

def p(d):
    for x in d:
        print(x.pretify())
        input()


def check(d):
    cand_idx = list(map(lambda x: x.idx-1 if x.reporter is None else None, d))
    cand_idx = list(filter(lambda x: x is not None, cand_idx))
    for x in cand_idx:
        print(d[x].pretify())
        input()



# %%
