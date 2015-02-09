# -*- coding: utf-8 -*-

import nltk


def lexical_diversity(text):                # Percent of unique words in corpus
    return len(set(text)) / float(len(text))


testset_tokens = reduce(lambda acc, lbl: acc + lbl.split(), testset.labels_processed, [])
ref_tokens = reduce(lambda acc, lbl: acc+lbl.split(), r.professions.label,[])

# Raw vocabularies
testset_voc = set(testset_tokens)
#  9629 types, diversity = 13%

ref_voc = set(ref_tokens)
#  4636 types, diversity = 6%

common_voc = testset_voc.intersection(ref_voc)
#  2722 types that appear in both vocabularies

# Stemmed vocabularies
stemmer = nltk.stem.snowball.FrenchStemmer()
testset_voc_stemmed = set([stemmer.stem(w) for w in testset_voc])
#  7751 types. Loss:

ref_voc_stemmed = set([stemmer.stem(w) for w in ref_voc])
#  4057

