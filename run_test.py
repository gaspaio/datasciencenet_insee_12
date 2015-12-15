# -*- coding: utf-8 -*-

import pandas as pd
import Referentiel as ref
#from ExactMatcher import ExactMatcher as Matcher
#from JaccardMatcher import JaccardMatcher as Matcher
from MasiMatcher import MasiMatcher as Matcher
from InseeRunner import InseeRunner
from RuleEngine import RuleEngine
import timeit
import os.path


if not os.path.isfile("pickles/referentiel.pkl"):
    print "Rebuilding referentiel. This will take a while."
    tb = timeit.default_timer()
    newref = ref.Referentiel()
    ref.save(newref)
    te = timeit.default_timer()
    print "Rebuilding time: {:.1f} seconds".format(te - tb)


if not os.path.isfile("pickles/testset_labels_processed.pkl"):
    print "Running rule engine on testset labels. This will take a while."
    tb = timeit.default_timer()
    rules = RuleEngine()
    test_set = pd.DataFrame.from_csv('data/professions_non_traitees.csv', sep=';', index_col=None)
    test_set.columns = ['id', 'labels']
    test_set['labels'] = test_set['labels'].apply(lambda x: x.decode('iso-8859-1'))
    test_set['labels_processed'] = test_set['labels'].apply(rules.apply_all)
    test_set.to_pickle("pickles/testset_labels_processed.pkl")
    te = timeit.default_timer()
    print "Rule engine run time: {:.1f} seconds".format(te - tb)

print "Loading objects"
referentiel = ref.load()
matcher = Matcher(referentiel)
test_set = pd.read_pickle("pickles/testset_labels_processed.pkl")

print "Running runner"
runner = InseeRunner(matcher, test_set['labels'], processed_inputs=test_set['labels_processed'])
runner.predict()
print "Running time: {:.1f} seconds".format(runner.time("predict"))

print "Exporting to csv"
out = runner.results[["libelle_1","libelle_2","libelle_3"]].fillna('')
out["idx"] = test_set["id"]
out.to_csv("testset_predictions.GOLDEN_BOY.csv", sep=";", index=False, columns=["idx", "libelle_1","libelle_2","libelle_3"], header=["ID", "Libelle 1", "Libelle 2", "Libelle 3"])
