# -*- coding: utf-8 -*-

import pandas as pd

from ExactMatcher import ExactMatcher

class TestExactMatcher(object):

    professions_compile_matches = [
        (u"COUCOU BINGO", u"COUCOU BINGO", True),
        (u"COUCOU BINGO", u"COUCOU BINGO BOINGO", False),
        (u"COUCOU BINGO", u"BOINGO COUCOU BINGO", False),
        (u"COUCOU $ BINGO", u"COUCOU BINGO", True),
        (u"COUCOU $ BINGO", u"COUCOU EXPLOITATION BINGO", True),
        (u"COUCOU $ BINGO", u"COUCOU EXPLOITATION SOMETHING BINGO", False),
        # (u"$ COUCOU BINGO", u"EXPLOITATION COUCOU BINGO", True),
        # (u"$ COUCOU BINGO", u"EXPLOITATION SOMETHING COUCOU BINGO", False),
        (u"COUCOU BINGO $", u"COUCOU BINGO", True),
        (u"COUCOU BINGO $", u"COUCOU BINGO EXPLOITATION", True),
        (u"COUCOU BINGO $", u"COUCOU BINGO EXPLOITATION SOMETHING", False),
        (u"COUCOU $2 BINGO", u"COUCOU BINGO", True),
        (u"COUCOU $2 BINGO", u"COUCOU EXPLOITATION BINGO", True),
        (u"COUCOU $2 BINGO", u"COUCOU EXPLOITATION SOMETHING BINGO", True),
        (u"COUCOU $2 BINGO", u"COUCOU EXPLOITATION SOMETHING OINGO BINGO", False),
        # (u"$2 COUCOU BINGO", u"COUCOU BINGO", False),
        # (u"$2 COUCOU BINGO", u"EXPLOITATION COUCOU BINGO", True),
        # (u"$2 COUCOU BINGO", u"EXPLOITATION SOMETHING COUCOU BINGO", True),
        # (u"$2 COUCOU BINGO", u"EXPLOITATION SOMETHING OINGO COUCOU BINGO", False),
        (u"COUCOU BINGO $2", u"COUCOU BINGO", True),
        (u"COUCOU BINGO $2", u"COUCOU BINGO EXPLOITATION", True),
        (u"COUCOU BINGO $2", u"COUCOU BINGO EXPLOITATION SOMETHING", True),
        (u"COUCOU BINGO $2", u"COUCOU BINGO EXPLOITATION SOMETHING OINGO", False),
        (u"COUCOU $3 BINGO", u"COUCOU BINGO", True),
        (u"COUCOU $3 BINGO", u"COUCOU EXPLOITATION BINGO", True),
        (u"COUCOU $3 BINGO", u"COUCOU EXPLOITATION OINGO BINGO", True),
        (u"COUCOU $3 BINGO", u"COUCOU EXPLOITATION SOMETHING OINGO BINGO", True),
        (u"COUCOU $3 BINGO", u"COUCOU EXPLOITATION SOMETHING OINGO LALA BINGO", False),
        # (u"$3 COUCOU BINGO", u"EXPLOITATION BINGO", False),
        # (u"$3 COUCOU BINGO", u"EXPLOITATION COUCOU BINGO", True),
        # (u"$3 COUCOU BINGO", u"EXPLOITATION OINGO COUCOU BINGO", True),
        # (u"$3 COUCOU BINGO", u"EXPLOITATION SOMETHING OINGO COUCOU BINGO", True),
        # (u"$3 COUCOU BINGO", u"EXPLOITATION SOMETHING OINGO LALA COUCOU BINGO", False),
        (u"COUCOU BINGO $3", u"COUCOU BINGO", True),
        (u"COUCOU BINGO $3", u"COUCOU BINGO EXPLOITATION", True),
        (u"COUCOU BINGO $3", u"COUCOU BINGO EXPLOITATION OINGO", True),
        (u"COUCOU BINGO $3", u"COUCOU BINGO EXPLOITATION SOMETHING OINGO", True),
        (u"COUCOU BINGO $3", u"COUCOU BINGO EXPLOITATION SOMETHING OINGO LALA", False),
        (u"COUCOU BING****", u"COUCOU BINGO", True),
        (u"COUCOU BING****", u"COUCOU BING", True),
        (u"COUCOU BING****", u"COUCOU BINGATITUDE", True),
        (u"COUCOU BING**** LALA", u"COUCOU BINGO LALA", True),
    ]

    @classmethod
    def setupClass(self):
        self.matcher = ExactMatcher(None)

    def test_compile(self):
       for item in TestExactMatcher.professions_compile_matches:
           yield self.check_compile, item[0], item[1], item[2]

    def check_compile(self, profession, label, should_match):
        data = pd.Series([profession])
        exp = self.matcher.compile(data)[0]
        out = exp.match(label)
        if should_match:
            errmsg = '"{}" didn\'t match "{}".'.format(profession, label)
        else:
            errmsg = '"{}" shoudn\'t match "{}".'.format(profession, label)
        assert bool(out) == should_match, errmsg
