# -*- coding: utf-8 -*-

from RuleEngine import RuleEngine

class TestRuleEngine(object):

    prepare_data = [
        (u"AGENT D'EXPLOITATION (SECURITE)", u"AGENT D EXPLOITATION SECURITE"),
        (u"NOUNOU GARDE D'ENFANT", u"NOUNOU GARDE D ENFANT"),
        (u"  NOUNOU    GARDE D'  ENFANT  ", u"NOUNOU GARDE D ENFANT"),
        (u"MAÇON", u"MACON"),
        (u"BIÈNGÙ", u"BIENGU"),
        (u"bingo èà&@ bibi$-", u"BINGO EA& BIBI"),
        (u"H&M COUCOU", u"H&M COUCOU")    # & is accepted, but filtered in the synonymes rules
    ]

    # Tests synonyms using the different types of rules
    rule_cases = [
        # Rule, label_in, out_out
        (("A A P","AAP"), u"QUELQUE A A P CHOSE", u"QUELQUE AAP CHOSE"),
        (("A A P","AAP"), u"QUELQUA A P CHOSE", u"QUELQUA A P CHOSE"),
        (("H&",""), u"QUELQUE H&M CHOSE", u"QUELQUE H&M CHOSE"),
        (("H&",""), u"QUELQUE H& CHOSE", u"QUELQUE CHOSE"),
        (("D",""), u"AGENT D EXPLOITATION SECURITE", u"AGENT EXPLOITATION SECURITE"),
        (("EN",""), u"STAGIAIRE EN ASSISTANCE SOCIAL", u"STAGIAIRE ASSISTANCE SOCIAL"),
        (("EN",""), u'EN ATTENTE', u'ATTENTE'),

        (("6CAT*","CATEGORIE6"), u'BIBI 6CATEGI LALA', u'BIBI CATEGORIE6 LALA'),
        (("P 1*","OQ"), u"SOMETHING P 123 BLBLA",u"SOMETHING OQ BLBLA"),
        (("6CAT*","CATEGORIE6"), u'BIBI 6CATEGI', u'BIBI CATEGORIE6'),
        (("6CAT*","CATEGORIE6"), u'BIBI 6CAT', u'BIBI CATEGORIE6'),
        (("6CAT*",""), u'BIBI 6CATEGI COUCOU', u'BIBI COUCOU'),
        (("6CAT*",""), u'BIBI 6CATEGI', u'BIBI'),
        (("6CAT*",""), u'6CATEGI BIBI', u'BIBI'),
        (("6CAT*",""), u'6CAT BIBI', u'BIBI'),

        (("IND* 8*", ""), u'INDIEHIPPIE 8FEETHAIR YOUNGSTER', "YOUNGSTER"),
        (("IND* 8*", ""), u'YOUNGSTER INDIEHIPPIE 8FEETHAIR', "YOUNGSTER"),
        (("IND* 8*", ""), u'INDIEHIPPIE 8FEETHAIR', ""),

        (("IND* NOUV* MAJ*", "INDICE"), u"INDIEHIPPIE NOUVEL MAJONG BUFF", u"INDICE BUFF"),
        (("IND* NOUV* MAJ*", "INDICE"), u"INDIEHIPPIE NOUVEL MAJONG BUFF", u"INDICE BUFF"),
        (("CONTRAT I* EMP*", ""), u"CONTRAT INTEMPOREL EMPOWERED", ""),
        #(("EBARDEU*";"EBARB*******"), u"EBARDEURME BINGO", "EB?"),

        # Patterns XXX * YYY
        (("OUVRIER * HAUTEMENT QUALIFIE","OQ *"), u"OUVRIER AGRICOLE HAUTEMENT QUALIFIE", "OQ AGRICOLE"),
        (("OUVRIER * HAUTEMENT QUALIFIE","OQ *"), u"OUVRIER HAUTEMENT QUALIFIE", "OQ"),
        (("OUVRIER * HAUTEMENT QUALIFIE","* OQ"), u"OUVRIER AGRICOLE HAUTEMENT QUALIFIE", "AGRICOLE OQ"),
        (("OUVRIER * HAUTEMENT QUALIFIE","* OQ"), u"OUVRIER HAUTEMENT QUALIFIE", "OQ"),
        (("OUVRIER * HAUTEMENT QUALIFIE","BIBI * OQ"), u"OUVRIER AGRICOLE HAUTEMENT QUALIFIE", "BIBI AGRICOLE OQ"),
        (("OUVRIER * HAUTEMENT QUALIFIE","BIBI * OQ"), u"OUVRIER HAUTEMENT QUALIFIE", "BIBI OQ"),
        (("OUVRIER * QUALIFIE",""), u"HOMME OUVRIER HAUTEMENT QUALIFIE CHINOIS", "HOMME CHINOIS"),

        # Patterns * XXX
        (("* HAUTEMENT QUALIFIE","OQ *"), u"AGRICOLE HAUTEMENT QUALIFIE", "OQ AGRICOLE"),
        (("* HAUTEMENT QUALIFIE","OQ *"), u"HAUTEMENT QUALIFIE", "OQ"),
        (("* HAUTEMENT QUALIFIE","* OQ"), u"AGRICOLE HAUTEMENT QUALIFIE", "AGRICOLE OQ"),
        (("* HAUTEMENT QUALIFIE","* OQ"), u"HAUTEMENT QUALIFIE", "OQ"),
        (("* HAUTEMENT QUALIFIE","BIBI * OQ"), u"AGRICOLE HAUTEMENT QUALIFIE", "BIBI AGRICOLE OQ"),
        (("* HAUTEMENT QUALIFIE","BIBI * OQ"), u"HAUTEMENT QUALIFIE", "BIBI OQ"),
        (("* QUALIFIE",""), u"HOMME HAUTEMENT QUALIFIE CHINOIS", "HOMME CHINOIS"),

        # Patterns XXX *
        (("HAUTEMENT QUALIFIE *","OQ *"), u"HAUTEMENT QUALIFIE AGRICOLE", "OQ AGRICOLE"),
        (("HAUTEMENT QUALIFIE *","OQ *"), u"HAUTEMENT QUALIFIE", "OQ"),
        (("HAUTEMENT QUALIFIE *","* OQ"), u"HAUTEMENT QUALIFIE AGRICOLE", "AGRICOLE OQ"),
        (("HAUTEMENT QUALIFIE *","* OQ"), u"HAUTEMENT QUALIFIE", "OQ"),
        (("HAUTEMENT QUALIFIE *","BIBI * OQ"), u"HAUTEMENT QUALIFIE AGRICOLE", "BIBI AGRICOLE OQ"),
        (("HAUTEMENT QUALIFIE *","BIBI * OQ"), u"HAUTEMENT QUALIFIE", "BIBI OQ"),
        (("QUALIFIE *",""), u"HOMME QUALIFIE HAUTEMENT CHINOIS", "HOMME CHINOIS"),

        # Patterns XXX ** YYY
        (("PROFESSEUR ** TITULAIRE", "PROFESSEUR SUPERCOOL **"), u"PROFESSEUR BLOND SYMPA TITULAIRE", u"PROFESSEUR SUPERCOOL BLOND SYMPA"),
        (("PROFESSEUR ** TITULAIRE", "PROFESSEUR SUPERCOOL **"), u"PROFESSEUR TITULAIRE", u"PROFESSEUR SUPERCOOL"),
        (("PROFESSEUR ** TITULAIRE", "** PROFESSEUR SUPERCOOL"), u"PROFESSEUR BLOND SYMPA TITULAIRE", u"BLOND SYMPA PROFESSEUR SUPERCOOL"),
        (("PROFESSEUR ** TITULAIRE", "** PROFESSEUR SUPERCOOL"), u"PROFESSEUR TITULAIRE", u"PROFESSEUR SUPERCOOL"),
        (("PROFESSEUR ** TITULAIRE", "PROFESSEUR ** SUPERCOOL"), u"PROFESSEUR BLOND SYMPA TITULAIRE", u"PROFESSEUR BLOND SYMPA SUPERCOOL"),
        (("PROFESSEUR ** TITULAIRE", "PROFESSEUR ** SUPERCOOL"), u"PROFESSEUR TITULAIRE", u"PROFESSEUR SUPERCOOL"),
        (("PROFESSEUR ** TITULAIRE", ""), u"TOUT PROFESSEUR BLOND SYMPA TITULAIRE VA BIEN", u"TOUT VA BIEN"),

        # Patterns ** YYY
        (("** PROFESSEUR TITULAIRE", "PROFESSEUR SUPERCOOL **"), u"BLOND SYMPA PROFESSEUR TITULAIRE", u"PROFESSEUR SUPERCOOL BLOND SYMPA"),
        (("** PROFESSEUR TITULAIRE", "PROFESSEUR SUPERCOOL **"), u"PROFESSEUR TITULAIRE", u"PROFESSEUR SUPERCOOL"),
        (("** PROFESSEUR TITULAIRE", "** PROFESSEUR SUPERCOOL"), u"BLOND SYMPA PROFESSEUR TITULAIRE", u"BLOND SYMPA PROFESSEUR SUPERCOOL"),
        (("** PROFESSEUR TITULAIRE", "** PROFESSEUR SUPERCOOL"), u"PROFESSEUR TITULAIRE", u"PROFESSEUR SUPERCOOL"),
        (("** PROFESSEUR TITULAIRE", "PROFESSEUR ** SUPERCOOL"), u"BLOND SYMPA PROFESSEUR TITULAIRE", u"PROFESSEUR BLOND SYMPA SUPERCOOL"),
        (("** PROFESSEUR TITULAIRE", "PROFESSEUR ** SUPERCOOL"), u"PROFESSEUR TITULAIRE", u"PROFESSEUR SUPERCOOL"),
        (("** PROFESSEUR", ""), u"TOUT VA BIEN PROFESSEUR TITULAIRE", u"TITULAIRE"),

        # Patterns XXX **
        (("PROFESSEUR TITULAIRE **", "PROFESSEUR SUPERCOOL **"), u"PROFESSEUR TITULAIRE BLOND SYMPA", u"PROFESSEUR SUPERCOOL BLOND SYMPA"),
        (("PROFESSEUR TITULAIRE **", "PROFESSEUR SUPERCOOL **"), u"PROFESSEUR TITULAIRE", u"PROFESSEUR SUPERCOOL"),
        (("PROFESSEUR TITULAIRE **", "** PROFESSEUR SUPERCOOL"), u"PROFESSEUR TITULAIRE BLOND SYMPA ", u"BLOND SYMPA PROFESSEUR SUPERCOOL"),
        (("PROFESSEUR TITULAIRE **", "** PROFESSEUR SUPERCOOL"), u"PROFESSEUR TITULAIRE", u"PROFESSEUR SUPERCOOL"),
        (("PROFESSEUR TITULAIRE **", "PROFESSEUR ** SUPERCOOL"), u"PROFESSEUR TITULAIRE BLOND SYMPA", u"PROFESSEUR BLOND SYMPA SUPERCOOL"),
        (("PROFESSEUR TITULAIRE **", "PROFESSEUR ** SUPERCOOL"), u"PROFESSEUR TITULAIRE", u"PROFESSEUR SUPERCOOL"),
        (("PROFESSEUR **", ""), u"TOUT VA BIEN PROFESSEUR TITULAIRE", u"TOUT VA BIEN"),

        # Rules with $A-Z
        (("ELEVE ADMIN*","$A ADMINIST"), u"MON ELEVE ADMINISTRATEUR",u"MON $A ADMINIST"),
        (("$A SECONDTECH", "$W SECONDTECH"), u"$A SECONDTECH QUELQUE PART", '$W SECONDTECH QUELQUE PART'),
        (("$* SECONDTECH", "$W SECONDTECH"), u"$R SECONDTECH QUELQUE PART", '$W SECONDTECH QUELQUE PART'),
        (("$A $Z", "$A"), u"COUCOU $A $Z HIHI", u"COUCOU $A HIHI"),
        (("$* $*", "$A"), u"COUCOU $A $Z HIHI", u"COUCOU $A HIHI"),

        # Mixing stuff
        (("OUVRIER* * HAUTEMENT QUALIFIE", "OQ *"), u"OUVRIERERE AGRICOLE HAUTEMENT QUALIFIE", "OQ AGRICOLE"),
        (("OUVRIER* ** HAUTEMENT QUALIFIE", "OQ **"), u"OUVRIERERE AGRICOLE JOLIE HAUTEMENT QUALIFIE", "OQ AGRICOLE JOLIE"),
        (("OUVRIER* ** HAUTEMENT * QUALIFIE", "OQ * **"), u"OUVRIERERE AGRICOLE JOLIE HAUTEMENT SYMPA QUALIFIE", "OQ SYMPA AGRICOLE JOLIE"),
        (("OUVRIER* ** HAUTEMENT *", "OQ * **"), u"OUVRIERERE AGRICOLE JOLIE HAUTEMENT SYMPA QUALIFIE", "OQ SYMPA AGRICOLE JOLIE QUALIFIE"),
        (("FP ** AGENTBURO", "$C AGENTBURO **"), u"JE SUIS FP MONSIEUR DOCTEUR AGENTBURO", u"JE SUIS $C AGENTBURO MONSIEUR DOCTEUR"),
        (("$* ** SECONDTECH", "$W SECONDTECH **"), u"$R QUELQUE PART SECONDTECH", '$W SECONDTECH QUELQUE PART'),
        (("CHERCHEUR ** DIREC* RECHERC*", "$A DIRECTEUR RECHERCHE **"), u"CHERCHEUR HIPI DIRECTEUR RECHERCHE", u"$A DIRECTEUR RECHERCHE HIPI"),
        (("CHERCHEUR ** DIREC* RECHERC*", "$A DIRECTEUR RECHERCHE **"), u"CHERCHEUR HIPI HURRA DIRECTEUR RECHERCHE", u"$A DIRECTEUR RECHERCHE HIPI HURRA"),
    ]

    # Test synonyms using the full ruleset
    ruleset_apply_data = [
        (u"HOTESSE D'AIR", u"HOTESSE AIR"),
        (u"GARDE D'ENFANTS AU DOMICILE", u"GARDIEN ENFANCE DOMICILE"),
        (u"CUISINIER / PIZZAIOLO", u"CUISINIER PIZZAIOLO"),
        (u"RESPONSABLE DE MAGASIN DE VENTE", "CHEF MAGASIN VENTE"),
        (u"INFORMATICIEN","INFORMATIQ"),
        (u"INFORMATICIENINHO","INFORMATIQ"),
    ]


    @classmethod
    def setupClass(self):
        self.engine = RuleEngine()

    def test_prepare_label(self):
        for item in TestRuleEngine.prepare_data:
            yield self.check_prepare_label, item[0], item[1]

    def test_compile(self):
        for case in TestRuleEngine.rule_cases:
            yield self.check_compile, case

    def test_apply_all(self):
        for case in TestRuleEngine.ruleset_apply_data:
            yield self.check_apply_all, case

    def check_apply_all(self, case):
        out = self.engine.apply_all(case[0])
        errmsg = '"{}" became "{}" instead of "{}"'.format(case[0], out, case[1])
        assert out == case[1], errmsg

    def check_compile(self, case):
        c_rule, repl = self.engine.compile(case[0])
        out = self.engine.apply(c_rule, repl, case[1])
        errmsg = 'applying rule {}: "{}" became "{}" instead of "{}"'.format(case[0], case[1], out, case[2])
        assert out == case[2], errmsg

    def check_prepare_label(self, label, expected):
        ret = self.engine.prepare_label(label)
        errmsg = u'{} became {} instead of {}'.format(label, ret, expected)
        assert ret == expected, errmsg
