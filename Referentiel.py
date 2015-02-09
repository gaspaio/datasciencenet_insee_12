# -*- coding: utf-8 -*-

import re
import pandas as pd
from RuleEngine import RuleEngine
import os.path
import pickle

def save(ref):
    pickle.dump(ref, open("pickles/referentiel.pkl", "wb"), protocol=pickle.HIGHEST_PROTOCOL)


def load():
    return pickle.load(open("pickles/referentiel.pkl", "rb"))


class Referentiel(object):

    #replace = {
        # "ADJOINT ADMINISTRATI 1ERE CLASSE $": "ADJOINT ADMINISTRATI CL1 $",
        # "ADJOINT ADMINISTRATI 2EME CLASSE $": "ADJOINT ADMINISTRATI CL2 $"
    #}



    def __init__(self):
        engine = RuleEngine()
        self.professions = self.import_referentiel("data/referentiel.csv")
        self.professions.columns = ["code", "label_orig"]
        self.professions['label'] = self.run_through_rules(self.professions.label_orig)

        #self.professions.label_orig.apply(lambda lorig: engine.apply_all(lorig.replace("$", "XYZ")).replace("XYZ", "$"))


    def run_through_rules(self, labels):

        vs_encode = {'$' : "XYZ",'*' : "ATX",}
        rx_encode = re.compile("(%s)" % "|".join(map(re.escape, vs_encode.keys())))
        vs_decode = {'XYZ': "$", 'ATX': "*"}
        rx_decode = re.compile("(%s)" % "|".join(map(re.escape, vs_decode.keys())))
        engine = RuleEngine()

        def apply_rules(label):
            l = rx_encode.sub(lambda mo: vs_encode[mo.string[mo.start():mo.end()]], label)
            l = engine.apply_all(l)
            return rx_decode.sub(lambda mo: vs_decode[mo.string[mo.start():mo.end()]], l)

        return labels.apply(apply_rules)



    def import_referentiel(self, filename):
        data = pd.DataFrame.from_csv(filename, index_col=None, sep=';')
        data.columns = ["code", "label"]

        # remove extra spaces
        exp = re.compile("  +")
        data['label'] = data.apply(lambda x: exp.sub(' ', x.label).strip(), axis=1)

        # replace some stuff
        #data.label.replace(to_replace=self.replace, inplace=True)

        return data


