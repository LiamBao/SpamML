# coding=utf-8

import datetime
import time
import traceback
import math
import ast
import logging
import socket
import multiprocessing


def current_pid():
    return multiprocessing.current_process().pid


def numlog(n, base=10, bias= -1):
    res = int(math.ceil(math.log(n + 1, base)))
    if bias >= 0 and n > bias:
        res += 10 
    return res


def userbasic(user, useshortdate=True):
    info = {}
    for i in ('friends_count', 'followers_count', 'statuses_count',
              'bi_followers_count', 'favourites_count'):
        info[i] = int(user.get(i, 0))
    info['created_at'] = useshortdate and shortdate(user['created_at']) or user['created_at']
    return info


def ratio_edge(n, m, nmin= -10, nmax=10):
    y = int(math.log(n / float(m + 1) + (1e-5), 10) * 10)
    if y < nmin:
        return nmin
    elif y > nmax:
        return nmax
    else:
        return y

    
def benchmark(f):
    def wrapper(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        logging.info('%s %f %s' % (f.__name__, time.time() - t, 'sec'))
        return res
    return wrapper


def tounicode(s):
    return isinstance(s, unicode) and s or isinstance(s, int) and unicode(s) or s.decode('utf-8')

def toutf8(s):
    return isinstance(s, unicode) and s.encode('utf-8') or isinstance(s, int) and str(s) or s


def get_normal_text(text):
    # 格式化字符串，去掉4字节的utf-8编码字符
    text_repr = repr(text)
    if text_repr.find('\\U000') != -1:
        text = re.sub('(\\\\U000\w+)', '', text_repr)
        text = eval(text)
        return text
    else:
        return text


def normalize(lst):
    total = float(sum(lst))
    if total <= 0:
        return lst
    else:
        return [i / total for i in lst]


def lstclosure():
    lst=[]
    def _(x=None):
        if x:
            lst.append(x)
        else:
            return lst
    return _


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def gen_rows(simple=False, fname='./training_data.txt'):
    with open(fname) as f:
        for i in f:
            line = i.strip().split(' : ')
            if len(line) != 3:
                continue
            uid, isspam, features = [ast.literal_eval(i) for i in line]
            features = simple and features[:10] or features
            yield [features, isspam, uid]

 
def get_timestamp(s):
    #'2010-09-01'
    ts = time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d").timetuple())
    return int(ts)


def now_str():
    return time.strftime('%Y-%m-%d %H:%M:%S %Z')


def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    ipaddr = s.getsockname()[0]
    s.close()
    return ipaddr
