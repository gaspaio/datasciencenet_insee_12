# -*- coding: utf-8 -*-

import re
import pandas as pd
from nltk.stem.snowball import FrenchStemmer
from nltk.metrics import jaccard_distance

class JaccardMatcher(object):

    rx_stem = re.compile(r"(?:.* |^)(?P<stem>\w+)(?P<wcs>\*+)(?: .*|$)")
    rx_rwc = re.compile(r" \$\d?")
    count = 0

    def __init__(self, referentiel = None):
        self.professions = None
        self.stemmer = FrenchStemmer()

        if referentiel:
            self.professions = referentiel.professions.copy()

            # Ignore labels with wildcards
            self.professions['label'] = self.professions.label.apply(lambda x: self.rx_rwc.sub('', x))
            self.professions.drop_duplicates(subset="label", inplace=True)

            # Stem everything
            self.professions['label'] = self.professions.label.apply(self.stemmer.stem)

            self.professions['label_types'] = self.professions['label'].apply(lambda s: set(s.split()))
            self.professions['stemmed_word'] = self.professions['label_types'].apply(self.stemmed_word)


    def match(self, label, k=3):
        """Returns a set of k matches for the label, ordered by score.

        returns [(precode, label, score), ...]
        """
        self.count += 1
        print "[{}] processing: {}".format(self.count, label)
        lbl_types = set(self.stemmer.stem(label).split())
        scores = self.professions.apply(lambda x: \
            self.score(lbl_types, x.label_types, x.stemmed_word), axis=1)

        res = self.professions[['label_orig', 'code']].copy()
        res['score'] = scores

        res = res.sort(columns="score", ascending=True)

        codes = []
        out = []
        for index, row in res.iterrows():
            if row.code in codes: continue
            codes.append(row.code)
            r = res.loc[index]
            out.append((r.code, r.label_orig, r.score))
            if len(codes) == k: break;

        return out


    def score(self, lbl_types, ref_types, stemmed_word):
        """Gives the Jaccard distance between the two sets."""
        if stemmed_word:
            ref_types = self.replace_stem(stemmed_word, ref_types, lbl_types)

        return jaccard_distance(lbl_types, ref_types)


    def replace_stem(self, stem, ref_types, lbl_types):
        """Replace the stemmed word in the ref types with the one occuring in lbl (if any)."""
        ls = len(stem)

        # Get word in label types
        lbl_w = next((x for x in lbl_types if x[0:ls] == stem), '')
        if not lbl_w: return ref_types

        # replace word in referentiel types
        s = stem + '*'
        ref_orig_w = next((x for x in ref_types if x[0:ls+1] == s), '')
        if ref_orig_w:
            ref_types.discard(ref_orig_w)
            ref_types.add(lbl_w)

        return ref_types


    def stemmed_word(self, ref_types):
        stemmed_word = None
        for t in ref_types:
            m = self.rx_stem.match(t)
            if m:
                stemmed_word = m.groupdict()['stem']
                break
        return stemmed_word

