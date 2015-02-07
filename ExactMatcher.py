# -*- coding: utf-8 -*-

import re
import pandas as pd

# TODO REMOVE DUPLICATE PROFESSIONS WITH $ and no $


class ExactMatcher(object):

    def __init__(self, referentiel = None):
        self.professions = None

        if referentiel:
            self.professions = referentiel.professions.copy()
            self.professions['label_compiled'] = self.compile(referentiel.professions['label'])

    def match(self, label, k=3):
        """Returns a set of k matches for the label, ordered by score.

        returns [(precode, label, score), ...]
        """
        # match label against referentiel
        match_idxs = self.professions['label_compiled'].apply(lambda exp: bool(exp.match(label)))

        # get matching label information, droping those with the same codes & keep only max K results
        results = self.professions[match_idxs].drop_duplicates(subset = 'code').head(3)
        # return list of tuples. We return the original referential label (r[1]), not the processed one (r[2]).
        return [(r[0], r[1], 1) for r in results.to_records(index=False)]

    def compile(self, professions):
        """Build a regex for each reference label."""
        ret = professions.replace({
            # Matching labels like "BINGO $ BONGO"
            # pattern = BINGO (\w+ )?BONGO
            re.compile(r"\$ "): r"(\w+ )?",

            # Matching labels like "BINGO BONGO $"
            # pattern = BINGO BONGO( \w+)?
            re.compile(r" \$$"): r"( \w+)?",

            # Matching labels like "BINGO $2 BONGO"
            # pattern = BINGO (\w+ ){0,2}BONGO
            re.compile(r"\$(?P<digit>\d) "): r"(\w+ ){0,\g<digit>}",

            # Matching labels like "BINGO BONGO $2"
            # pattern = BINGO BONGO( \w+){0,2}
            re.compile(r" \$(?P<digit>\d)$"): r"( \w+){0,\g<digit>}",

            # Matching words like BING**** BINGO
            # pattern = BING\w+ BINGO
            re.compile(r"\*+(?P<sep> |$)"): r"\w*\g<sep>"
            })

        return ret.apply(lambda e: re.compile(r'^' + e + r'$'))
