# coding: utf-8

import numpy as np
from sklearn import svm
from sklearn import preprocessing

NUM_FEATURES = [14, 10]

class SVMer(object):
    def __init__(self, simple=False):
        self.cls()
        self.scaler = None
        self.simple = simple
        C, gamma = 3, 0.3  # grid test values
        self.clf = svm.SVC(C=C, gamma=gamma, class_weight='balanced')
    
    def fit(self):
        X, y = self.pre()
        self.clf.fit(X, y)
        self.cls()
    
    def predict(self):
        X, y = self.pre()
        print 'svm training score:', self.clf.score(X, y)
        self.scaler = None
        
    def judge(self, stats=False):
        X, y = self.pre()
        if stats:
            y_ = self.clf.predict(X)
            dic = {}
            for i, j in zip(self.y, y_):
                s = '%s_%s' % (i,j)
                dic.setdefault(s, 0)
                dic[s] += 1
            P = dic['1_1'] * 1. / ((dic['1_1'] + dic['0_1']) or 1)
            R = dic['1_1'] * 1. / ((dic['1_1'] + dic['1_0']) or 1)
            f1 = 2.0 * P * R / ((P + R) or 1)
            print 'dic:', dic
            print 'Precision:%s, Recall: %s, f1: %s, N: %s' % (P, R, f1, sum(dic.values()))
        self.cls()
        if X.any() != None:
            return self.clf.predict(X)[0]
        else:
            return -1
    
    def add(self, X, y, uid):
        if len(X) != NUM_FEATURES[self.simple]:
            raise Exception('row num %d is not %d, uid: %s' % (len(X), NUM_FEATURES[self.simple], uid), X)
        self.X.append(X)
        self.y.append(y)
        self.uids.append(uid)
        
    def pre(self):
        try:   
            X = np.array(self.X, dtype=float)   
        except Exception, e:
            print self.X 
            print self.uids
            self.cls()
            raise e
        y = np.array(self.y)
        if not self.scaler:
            self.scaler = preprocessing.StandardScaler().fit(X)
        try:
            X = self.scaler.transform(X)  # scaler can be used later for prediction
        except:
            print 'transform error, X is:' , X
            self.cls()
            return None, None
        return X, y
    
    def cls(self):
        self.X, self.y, self.uids = [], [], []
                    
