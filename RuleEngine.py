# -*- coding: utf-8 -*-

import re
from unidecode import unidecode

import pandas as pd

class RuleEngine(object):
    """Does all the mechanical processing of a label.

    - Label cleanup
    - Apply all the synonymes rules & return the resulting label
    """

    # We'll replace the original rule by a new version
    # TODO: refactor
    replaced_rules = {
        ("**( SANS", "**("): ("** SANS", "**"),
        ("**( A", "$A **"): ("** A", "$A **"),
        ("**( B", "$B **"): ("** B", "$B **"),
        ("**( C", "$C **"): ("** C", "$C **"),
        ("**( CORPS", "**"): ("** CORPS", "**"),
        ("**( GRADE", "**"): ("** GRADE", "**"),
    }

    # Some rule seem either useless, either uncomprehensible.
    # We'll just ignore them for now
    ignored_rules = [
        # Useless: no possible match in test data
        ("EBARDEU*", "EBARB*******"),

        ("**( D", "$D **"),

        # WTF ??
        ("*X *Y *Z ** *X *Y *Z", "*X *Y *Z **"),
        ("*X *Y *Z *X *Y *Z", "*X *Y *Z"),
        ("*X *Y ** *X *Y", "*X *Y **"),
        ("*X *Y *X *Y", "*X *Y"),
        ("*X ** *X", "*X **"),
        ("*X ** *X", "*X **"),
        ("*X *X", "*X"),
        ("$W", "**"),
        ("$3", "$ $ $"),
        ("$2", "$ $"),
        ("$", "************")
    ]

    # Pre-compiled utilitary regexes
    whitespace_cleanup = re.compile('  +')
    ignored_chars = re.compile('[^A-Z0-9& ]')

    def __init__(self, rule_file='data/synonymes.csv'):
        self.rules = None
        if not rule_file: return
        self.rules = self.import_rules(rule_file)
        self.compile_rules()

    def import_rules(self, filepath):
        """Import synonymes file into the rules DF."""
        synonymes = pd.DataFrame.from_csv(filepath, sep=';', index_col=None, header=None).fillna('')
        synonymes.columns = ['pat', 'repl']

        # remove ignored rules
        idx_tokeep = synonymes.apply(lambda r: (r['pat'], r['repl']) not in RuleEngine.ignored_rules, axis=1)
        synonymes = synonymes[idx_tokeep].copy()

        # replace certain rules
        for i, r in synonymes.iterrows():
            if (r.pat, r.repl) in RuleEngine.replaced_rules.keys():
                synonymes.loc[i] = RuleEngine.replaced_rules[(r.pat, r.repl)]

        return synonymes

    def apply(self, compiled_rule, replacement, label):
        result = compiled_rule.sub(replacement, label)
        return RuleEngine.whitespace_cleanup.sub(' ', result).strip()

    def apply_all(self, label):
        clean_label = self.prepare_label(label)
        return reduce(lambda acc, y: self.apply(y[3], y[4], acc), self.rules.itertuples(), clean_label)

    def prepare_label(self, label):
        """Cleanup the label: upper, remove exotic chars, transliterate."""
        # TRANSLITERATE
        # Basic transliteration. Doesn't correctly handle wierd cases like ^2 (from test file)
        label = unidecode(label)
        label = label.upper()
        # Remove out of range chars & extra whitespaces
        label = RuleEngine.ignored_chars.sub(' ', label)
        # remove extra whitespaces
        label = RuleEngine.whitespace_cleanup.sub(' ',label).strip()

        return label

    def compile_rules(self):
        """Compile all the rules in the synonymes datafile into regexes.

        Adds 2 cols to the self.rules DF: the compiled regex object and the replacement string.
        """
        self.rules['rule'], self.rules['replacement'] = \
            zip(*self.rules.apply(lambda x: self.compile((x.pat, x.repl)), axis=1))

    def compile(self, rule):
        """Build a compiled regex and the associated replacement pattern.

        rule: (pattern, replacement)

        returns: regex, replacement
        """
        pat = rule[0]
        repl = rule[1]

        # $ is a reserved char in a regex
        pat = pat.replace('$','\$')

        # Patterns in the form XXX* ou XXX***
        if re.search(r"[A-Z0-9$]+\*+", pat):
            pat = re.sub(r"(?P<wxt>[A-Z0-9$]+)\*+", r"\g<wxt>[A-Z0-9]*", pat)

        # Single word matches: XXX * YYY, XXX *, * YYY
        # TODO Make this prettier
        swg = re.search(r"( |^)\*( |$)", pat)
        if swg:
            # '*' pattern: doesn't make sense
            if '' == swg.group(1) == swg.group(2):
                raise Exception, "'{}' rule is strange".format(rule[0])
            # 'XXX * YYY' pattern
            elif ' ' == swg.group(1) == swg.group(2):
                pat = re.sub(r" \* ", r"(?P<swg> (?:\w+ )?)", pat)
            # '* YYY' pattern
            elif '' == swg.group(1):
                pat = re.sub(r"^\* ", r"(?P<swg>(?:\w+ )?)", pat)
            # 'XXX *' pattern
            else:
                pat = re.sub(r" \*$", r"(?P<swg>(?: \w+)?)", pat)

            repl = re.sub(r"( |^)\*( |$)", r" \\g<swg> ", repl)

        # Multiple word matches: XXX ** YYY, XXX **, ** YYY
        mwg = re.search(r"( |^)\*\*+( |$)", pat)
        if mwg:
            # '**' pattern doesn't make sense
            if '' == mwg.group(1) == mwg.group(2):
                raise Exception, "'{}' rule is strange".format(rule[0])
            # 'XXX ** YYY' pattern
            elif ' ' == mwg.group(1) == mwg.group(2):
                pat = re.sub(r" \*\*+ ", r"(?P<mwg> (?:\w+ )*)", pat)
            # '** YYY' pattern
            elif '' == mwg.group(1):
                pat = re.sub(r"^\*\*+ ", r"(?P<mwg>(?:\w+ )*)", pat)
            # 'XXX **' pattern
            else:
                pat = re.sub(r" \*\*+$", r"(?P<mwg>(?: \w+)*)", pat)

            repl = re.sub(r"( |^)\*\*+( |$)", r" \\g<mwg> ", repl)

        # magic corrections (compensated by the trim & regex below)
        repl = " {} ".format(repl)
        pat = r"(?: |^){}(?: |$)".format(pat)

        return re.compile(pat), repl






