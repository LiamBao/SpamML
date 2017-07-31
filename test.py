from spammer import is_spam
import ast

def test(fname='./test_data.txt'):
    with open(fname) as f:
        for l in f:
            uid, row = ast.literal_eval(l.strip())
            uid = str(uid)
            print uid, row, is_spam(row, uid)

if __name__ == "__main__":
    test()
