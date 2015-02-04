# -*- coding: utf-8 -*-

import pandas as pd
from RuleEngine import RuleEngine

class InseeRunner(object):

    def __init__(self, matcher, inputs, expected = None, k=3):
        self.matcher = matcher
        self.rules = RuleEngine()
        # A Series of input labels
        self.input = inputs
        # A Series of correct labels
        self.expected = expected
        self.k = k

        self.result_cols = []
        for i in range(self.k):
            self.result_cols.append('libelle_' + str(i+1))
            self.result_cols.append('code_' + str(i+1))
            self.result_cols.append('score_' + str(i+1))
        self.results = None


    def predict_label(self, label):
        label = self.rules.apply_all(label)
        return self.matcher.match(label, self.k)


    def predict(self):
        res = map(self.flaten_matches, self.input.apply(self.predict_label))
        self.results = pd.DataFrame(res, columns=self.result_cols)


    def flaten_matches(self, matches):
        ret = [None] * (self.k * 3)
        for i in range(len(matches)):
            if i > self.k:
                print("WARNING: match number greater than K")
                break
            ret[i*3] = matches[i][1]
            ret[i*3+1] = matches[i][0]
            ret[i*3+2] = matches[i][2]
        return ret


#    def accuracy():
