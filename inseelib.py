# -*- coding: utf-8 -*-

import pandas as pd
from Referentiel import Referentiel
#from RuleEngine import RuleEngine
from MechanicalMatcher import MechanicalMatcher
from InseeRunner import InseeRunner

ref = Referentiel()
mec_matcher = MechanicalMatcher(ref)

exemples = pd.DataFrame.from_csv('data/exemples.csv', sep=';', index_col=None, encoding='utf-8')
exemples.columns = ['label', 'expected']

runner = InseeRunner(mec_matcher, exemples.label)
runner.predict()

print runner.results.head()



