import classify
import ast
from utils import gen_rows

               
def prepare():
    import numpy as np
    res = []
    for simple in (False, True):
        cls = classify.SVMer(simple=simple)
        res.append(cls)
        for row in gen_rows(simple):
            cls.add(*row)
        cls.fit()
    return res

gSpamer, gSpamersimple = prepare()
assert gSpamer
assert gSpamersimple
