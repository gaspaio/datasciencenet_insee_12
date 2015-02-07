import pandas as pd
from InseeRunner import InseeRunner
from Referentiel import Referentiel
from MechanicalMatcher import MechanicalMatcher

ref = Referentiel()
matcher = MechanicalMatcher(ref)
dataset = pd.read_pickle('professions_non_traitees.pkl')

runner = InseeRunner(matcher, dataset['labels'])
runner.apply_rules()

runner.data.to_pickle('professions_non_traitees.clean.pkl')

