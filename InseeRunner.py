# -*- coding: utf-8 -*-

import pandas as pd
from RuleEngine import RuleEngine
import timeit

class InseeRunner(object):

    def __init__(self, matcher, inputs, processed_inputs = [], expected = None, k=3):
        self.matcher = matcher
        self.rules = RuleEngine()

        # A Series of input labels
        data = {'labels_input': inputs}
        if processed_inputs:
            data['labels_processed'] = processed_inputs
        self.data = pd.DataFrame(data)

        self.data.columns = ['labels_input']

        # A Series of correct labels
        self.expected = expected
        self.k = k

        self.result_cols = []
        for i in range(self.k):
            self.result_cols.append('libelle_' + str(i+1))
            self.result_cols.append('code_' + str(i+1))
            self.result_cols.append('score_' + str(i+1))

        self.results = None
        self.timer = {}


    def predict_label(self, label):
        label = self.rules.apply_all(label)
        return self.matcher.match(label, self.k)


    def apply_rules(self):
        self.start_timer('process_labels')
        self.data['labels_processed'] = self.data.labels_input.apply(self.rules.apply_all)
        self.stop_timer('process_labels')


    def predict(self, force_apply_rules=False):
        self.start_timer('predict')

        if 'labels_processed' not in self.data or force_apply_rules:
            self.apply_rules()

        res = map(self.flaten_matches, self.data.labels_processed.apply(self.matcher.match, k=self.k))
        self.results = pd.DataFrame(res, columns=self.result_cols)
        self.stop_timer('predict')


    def flaten_matches(self, matches):
        ret = [None] * (self.k * 3)
        for i in range(len(matches)):
            ret[i*3] = matches[i][1]
            ret[i*3+1] = matches[i][0]
            ret[i*3+2] = matches[i][2]
        return ret


    def performance(self):
        predicted = self.results['libelle_1']
        right = sum([(bool(lbl) and lbl == self.expected[idx]) \
                        for idx, lbl in enumerate(predicted)])
        expected = self.expected
        wrong = sum([(bool(lbl) and expected[idx] != lbl) \
                        for idx, lbl in enumerate(predicted)])
        return {
            'right guesses': right,
            'wrong guesses': wrong,
            'set size': len(expected),
            'accuracy': float(right)/len(expected),
            'time': self.time('predict')
        }


    def start_timer(self, key = 'default'):
        self.timer[key] = [timeit.default_timer(), 0]
        return


    def stop_timer(self, key):
        self.timer[key][1] = timeit.default_timer()
        return self.time(key)


    def time(self, key):
        if not self.timer[key][1]:
            return timeit.default_timer() - self.timer[key][0]
        return self.timer[key][1] - self.timer[key][0]

