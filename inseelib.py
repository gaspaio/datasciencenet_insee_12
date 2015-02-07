# -*- coding: utf-8 -*-

import pandas as pd
import Referentiel as ref
from ExactMatcher import ExactMatcher
from InseeRunner import InseeRunner
from InseeRunner import get_expected_codes
import os.path

if not os.path.isfile("pickles/referentiel.pkl"):
    print "Rebuilding referentiel. This will take a while."
    newref = ref.Referentiel()
    ref.save()

print "Loading objects"
referentiel = ref.load()
exact_matcher = ExactMatcher(referentiel)

print "Loading data"
exemples = pd.DataFrame.from_csv('data/exemples.csv', sep=';', index_col=None, encoding='utf-8')
exemples.columns = ['label', 'expected']
exemples['expected_codes'] = get_expected_codes(exemples.expected, referentiel)

print "Running runner"
runner = InseeRunner(exact_matcher, exemples.label, expected=exemples.expected_codes)
runner.predict()

print runner.trainperf()
