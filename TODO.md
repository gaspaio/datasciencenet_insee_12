# TODO
## stupid matching
- convert $A ... $Z to their labels
- convert referenciel to regex
- group by code
- trunc words to 20 chars
- matcher: if label matches exactly on label in a group, set code.

## better matcher
- same thing but stemm referentiel & labels
- remove duplicates after stemming
- groups labels in same group

# Mechanical matching
- X : Apply rules to train data & do matching
- Build runner:
- X > takes an iterable of labels
- X > inits all objects
- X > runs matching
- > -> and returns table with suggestions (3 best)
- > -> write to file using correct output format

- > if +50%: apply rules to test dataset & get score
- understand referenciel & better matching with wildcards

- look at non matched items in training set

# Fuzzy matching
- match by distance & propose different candidates
- Jacardi distance: count common words, http://bommaritollc.com/2014/06/advanced-approximate-sentence-matching-python/ (scores 0.0 - 1.0)

# TODO LATER
Test all items in referenciel through the ruleset. They shouldn't change.
If they change, there are errors somewhere.

## check weird cases in examples :
- AUXILIAIRE DE PUERICULTURE 3014 9 03 9 99;AUXILIAIRE PUERICULT
- TECHNICIEN EN TP;TECHNICIEN TP 
    => n'existe pas dans le ref. Dans le ref on a TECHNICIEN TP CATEGORIE B


# Corrections Referentiel
276 1ERE CLASSE -> CL1
277 2EME CLASSE -> CL2
