# -*- coding: utf-8 -*-

import re
import pandas as pd

class Referentiel(object):

    def __init__(self, ref_file='data/referenciel'):
        self.data = self.import_referentiel(ref_file)

    def import_referentiel(self, filename):
        data = pd.DataFrame.from_csv('data/referentiel.csv', index_col=None, sep=';')
        data.columns = ["code", "label"]

        # remove extra spaces
        exp = re.compile('  +')
        data['label'] = data.apply(lambda x: exp.sub(' ', x.label).strip(), axis=1)

        return data

