# -*- coding: utf-8 -*-

import re
import pandas as pd

class JaccardMatcher(object):

    rx_wcs = re.compile(r".+ \$(?P<dig>\d)?.*$")
    rx_stem = re.compile(r"(?:.* |^)(?P<stem>\w+)(?P<wcs>\*+)(?: .*|$)")
    count = 0

    def __init__(self, referentiel = None):
        self.professions = None

        if referentiel:
            self.professions = referentiel.professions.copy()
            self.professions['label_types'] = self.professions['label'].apply(lambda s: set(s.split()))
            self.professions['wildcard'] = self.professions['label'].apply(self.wildcard_count)
            self.professions['stemmed_word'] = self.professions['label_types'].apply(self.stemmed_word)


    def match(self, label, k=3):
        """Returns a set of k matches for the label, ordered by score.

        returns [(precode, label, score), ...]
        """
        self.count += 1
        print "[{}] processing: {}".format(self.count, label)
        lbl_types = set(label.split())
        scores = self.professions.apply(lambda x: \
            self.modified_jaccard_index(lbl_types, x.label_types, x.wildcard, x.stemmed_word), axis=1)

        res = self.professions[['label_orig', 'code']].copy()
        res['score'] = scores

        # This is way too heavy. We're grouping and ordering the whole set just to get three results ...
        #scores_by_code = res.groupby("code", as_index=False).apply(\
        #    lambda g: g.loc[g.sort(columns="score", ascending=False).index[0]]).sort(columns="score", ascending=False)
        #return [(r[1], r[0], r[2]) for r in scores_by_code.head(k).to_records(index=False)]

        res = res.sort(columns="score", ascending=False)

        codes = []
        idxs = []
        for index, row in res.iterrows():
            if row.code in codes: continue
            codes.append(row.code)
            idxs.append(index)
            if len(codes) == k: break;

        out = []
        for idx in idxs:
            r = res.loc[idx]
            out.append((r.code, r.label_orig, r.score))

        return out


    def modified_jaccard_index(self, lbl_types, ref_types, wildcard_count, stemmed_word):

        if stemmed_word:
            ref_types = self.replace_stem(stemmed_word, ref_types, lbl_types)

        num = len(lbl_types.intersection(ref_types))
        denom = len(lbl_types.union(ref_types))

        if wildcard_count:
            num = min(num + wildcard_count, len(lbl_types))
            denom -= 1

        return num/float(denom)


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



    def wildcard_count(self, ref_label):
        m = self.rx_wcs.match(ref_label)
        if not m: return 0
        elif m.groups()[0] == None: return 1
        else: return int(m.groups()[0])


    def stemmed_word(self, ref_types):
        stemmed_word = None
        for t in ref_types:
            m = self.rx_stem.match(t)
            if m:
                stemmed_word = m.groupdict()['stem']
                break
        return stemmed_word

