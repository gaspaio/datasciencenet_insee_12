# -*- coding: utf-8 -*-

import pandas as pd
import Referentiel as ref
from ExactMatcher import ExactMatcher
from JaccardMatcher import JaccardMatcher
from InseeRunner import InseeRunner
from InseeRunner import get_expected_codes
import os.path

if not os.path.isfile("pickles/referentiel.pkl"):
    print "Rebuilding referentiel. This will take a while."
    newref = ref.Referentiel()
    ref.save(newref)

print "Loading objects"
referentiel = ref.load()
#exact_matcher = ExactMatcher(referentiel)
matcher = JaccardMatcher(referentiel)

print "Loading data"
exemples = pd.DataFrame.from_csv('data/exemples.csv', sep=';', index_col=None, encoding='utf-8')
exemples.columns = ['labels', 'expected']
exemples['expected_codes'] = get_expected_codes(exemples.expected, referentiel)

print "Running runner"
runner = InseeRunner(matcher, exemples['labels'], expected=exemples['expected_codes'])
runner.predict()

print runner.trainperf()

print "Exporting to csv"
out = runner.results[["libelle_1","libelle_2","libelle_3"]].fillna('')
#out["idx"] = test_set["id"]
out.to_csv("trainset_predictions.csv", sep=";", columns=["libelle_1","libelle_2","libelle_3"], header=["Libelle 1", "Libelle 2", "Libelle 3"])
