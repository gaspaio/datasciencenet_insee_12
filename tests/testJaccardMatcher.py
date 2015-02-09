# -*- coding: utf-8 -*-

import pandas as pd

from JaccardMatcher import JaccardMatcher

class TestJaccardMatcher(object):

    jaccard_labels = [
        ("BINGO OINGO COUCOU", 0, None, "BINGO ZUZU COUCOU", 0.5),
        ("1ER MARINE NATIONALE MAITRE $", 1, None, "1ER MARINE NATIONALE MAITRE BONGO", 1),
        ("1ER MARINE NATIONALE MAITRE $", 1, None, "1ER MARINE NATIONALE MAITRE", 1),
        ("1ER MARINE NATIONALE MAITRE $", 1, None, "1ER MARINE NATIONALE ZUT BINGO", 4/6.0), # intercep: ("1ER", "MARINE", "NATINALE", "ZUT"),
                                                                                    # union: ("1ER", "MARINE", "NATINALE", "ZUT", "MAITRE", "BINGO")
        ("1ER MARINE $ NATIONALE MAITRE", 1, None, "1ER MARINE NATIONALE ZUT BINGO", 4/6.0),
        ("1ER MARINE $ NATIONALE MAITRE", 1, None, "NATIONALE ZUT BINGO", 2/6.0),  # intercept: (NATIONALE, ZUT)
                                                                          # union: (1ER, MARINE, NATIONALE, ZUT, BINGO, MAITRE)

        ("AAP CCP $3", 3, None, "AAP CCP", 1),                               # i=2 -> 2, u=3 -> 2   i=min(5,2)
        ("AAP CCP $3", 3, None, "AAP CCP BINGO", 1),                         # i=2 -> 3, u=4 -> 3   i=min(5,3)
        ("AAP CCP $3", 3, None, "AAP CCP BINGO COUCOU", 1),                  # i=2 -> 4, u=5 -> 4   i=min(5,4)
        ("AAP CCP $3", 3, None, "AAP CCP BINGO COUCOU LALA", 1),             # i=2 -> 5, u=6 -> 5   i=min(5,5)
        ("AAP CCP $3", 3, None, "AAP CCP BINGO COUCOU LALA ZUZU", 5/6.0),    # i=2 -> 5, u=7 -> 6   i=min(5,6)
        ("AAP CCP $3", 3, None, "AAP BINGO COUCOU LALA ZUZU", 4/6.0),        # i=1 -> 4, u=7 -> 6   i=min(4,5)

        ("BINGO OINGO COUC**", 0, "COUC", "BINGO ZUZU COUCOU", 0.5),
        ("BINGO COUC****", 0, "COUC", "BINGO COUCOU", 1),
        ("BINGO COUC**** BLABLA", 0, "COUC", "BINGO COUCOU BLABLA", 1),
        ("1ER MARINE $ NATIONALE MAIT****", 1, None, "1ER MARINE NATIONALE ZUT BINGO", 4/6.0),
        ("1ER MARINE $ NATION**** MAITRE", 1, "NATION", "1ER MARINE NATIONALE ZUT BINGO", 4/6.0),
    ]

    stem_replace = [
        ("LIL", set(["COUCOU", "BINGO", "LIL****"]), set(["FIFI", "RIRI", "LILI"]), set(["COUCOU", "BINGO", "LILI"])),
        ("LIL", set(["COUCOU", "BINGO", "LIL**"]), set(["FIFI", "RIRI", "LILI"]), set(["COUCOU", "BINGO", "LILI"])),
        ("TP", set(["CHARGE", "AFFAIRE", "INGENIEUR", "TP*", "CATEGORIE A"]), set(["CHEFEQUIPE", "TP"]), set(["CHARGE", "AFFAIRE", "INGENIEUR", "TP", "CATEGORIE A"]))
    ]


    @classmethod
    def setupClass(self):
        self.matcher = JaccardMatcher(None)


    def test_wildcard_count(self):
        assert self.matcher.wildcard_count("BINGO LALA") == 0
        assert self.matcher.wildcard_count("BINGO LALA $") == 1
        assert self.matcher.wildcard_count("BINGO LALA $2") == 2
        assert self.matcher.wildcard_count("BINGO LALA $3") == 3
        assert self.matcher.wildcard_count("BINGO $ LALA") == 1
        assert self.matcher.wildcard_count("BINGO $2 LALA") == 2
        assert self.matcher.wildcard_count("BINGO $3 LALA") == 3


    def test_stemmed_word(self):
        assert self.matcher.stemmed_word(set(["BINGO", "LALA"])) == None
        assert self.matcher.stemmed_word(set(["BINGO", "LALA****"])) == "LALA"
        assert self.matcher.stemmed_word(set(["BINGO", "LALA**", "COUCOU"])) == "LALA"


    def test_replace_stem(self):
       for item in self.stem_replace:
           yield self.check_replace_stem, item[0], item[1], item[2], item[3]


    def test_modified_jaccard_index(self):
       for item in self.jaccard_labels:
           yield self.check_modified_jaccard_index, item[0], item[1], item[2], item[3], item[4]


    def check_replace_stem(self, stem, reftypes_orig, lbltypes, reftypes_final):
        out = self.matcher.replace_stem(stem, reftypes_orig, lbltypes)
        assert out == reftypes_final


    def check_modified_jaccard_index(self, ref, wc, sw, lbl, idx):
        out = self.matcher.modified_jaccard_index(set(lbl.split()), set(ref.split()), wc, sw)
        errmsg = '"{}" and "{}" should have a Jaccard index of {:.2f}, got {:.2f}'.format(lbl, ref, idx, out)
        assert out == idx, errmsg

