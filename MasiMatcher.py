# -*- coding: utf-8 -*-

from nltk.metrics import masi_distance

from JaccardMatcher import JaccardMatcher


class MasiMatcher(JaccardMatcher):

    def score(self, lbl_types, ref_types, stemmed_word):
        """Gives the Masi distance between the two sets."""
        if stemmed_word:
            ref_types = self.replace_stem(stemmed_word, ref_types, lbl_types)

        return masi_distance(lbl_types, ref_types)
