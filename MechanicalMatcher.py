# -*- coding: utf-8 -*-

import re
import pandas as pd

class MechanicalMatcher(object):

    def __init__(self, referentiel):
        self.referentiel = referentiel

    def match(self, label, k):
        """Returns a set of k matches for the label, ordered by score.

        returns [(precode, label, score), ...]
        """
        results = self.referentiel.data.label[self.referentiel.data.label == label].index.tolist()

        ret = []

        if results:
            res = self.referentiel.data.loc[results[0]]
            ret.append((res.code, res.label, 1))

        return ret
