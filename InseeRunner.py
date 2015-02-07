# -*- coding: utf-8 -*-

import pandas as pd
import timeit

from RuleEngine import RuleEngine


def get_expected_codes(expected_labels, ref):

    def get_indexes(l, r):
        d = r.professions[r.professions.label_orig == l]
        if d.empty: return None
        else: return r.professions.loc[d.index[0]].code

    return expected_labels.apply(get_indexes,r = ref)


class InseeRunner(object):

    testset_filename = "data/professions_non_traitees.csv"

    def __init__(self, matcher, inputs, processed_inputs = pd.DataFrame(), expected = None, k=3):
        self.matcher = matcher
        self.rules = RuleEngine()

        # A Series of input labels
        data = {'labels_input': inputs}
        if not processed_inputs.empty:
            data['labels_processed'] = processed_inputs
        self.data = pd.DataFrame(data)

#        self.data.columns = ['labels_input']

        # A Series of correct codes
        self.expected = expected
        self.k = k

        self.result_cols = []
        for i in range(self.k):
            self.result_cols.append('code_' + str(i+1))
            self.result_cols.append('libelle_' + str(i+1))
            self.result_cols.append('score_' + str(i+1))

        self.results = None
        self.timer = {}


    def predict(self, force_apply_rules=False):
        self.start_timer('predict')

        if 'labels_processed' not in self.data or force_apply_rules:
            self.apply_rules()

        # Gives a Series of match lists of tuples (yes, it's overly complicated)
        res = self.data.labels_processed.apply(self.matcher.match, k=self.k)
        # Build return dataframe
        self.results = pd.DataFrame(res.apply(self.flatten).tolist(), columns=self.result_cols)

        self.stop_timer('predict')


    def trainperf(self):
        predicted = self.results['code_1']
        right = sum([(bool(code) and code == self.expected[idx]) \
                        for idx, code in enumerate(predicted)])
        expected = self.expected
        wrong = sum([(bool(code) and code != expected[idx]) \
                        for idx, code in enumerate(predicted)])
        return {
            'right guesses': right,
            'wrong guesses': wrong,
            'set size': len(expected),
            'accuracy': float(right)/len(expected),
            'time': self.time('predict')
        }


    def predict_label(self, label):
        label = self.rules.apply_all(label)
        return self.matcher.match(label, self.k)


    def apply_rules(self):
        self.start_timer('process_labels')
        self.data['labels_processed'] = self.data.labels_input.apply(self.rules.apply_all)
        self.stop_timer('process_labels')

    # Utilities

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


    def flatten(self, tpl):
        """Flaten a tuple list into a simple list of fixed length (k), padding with None."""
        out = [i  for item in tpl for i in item]
        return out + [None]*(self.k*3 - len(out))
