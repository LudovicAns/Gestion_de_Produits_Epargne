class Personne:

    def __init__(self, nom, age, revenu_annuel, loyer, depenses_mensuelle, objectif, duree_epargne, versement_mensuel_utilisateur = 0):
        self.nom = nom
        self.age = age
        self.revenu_annuel = revenu_annuel
        self.loyer = loyer
        self.depenses_mensuelle = depenses_mensuelle
        self.objectif = objectif
        self.duree_epargne = duree_epargne
        self.versement_mensuel_utilisateur = versement_mensuel_utilisateur

    def __str__(self):
        return (f"{self.nom} {self.age} ans, a un revenu annuel de {self.revenu_annuel} €.\n"
                f"Paye un loyer de {self.loyer} € par mois, et a une depense mensuelle de {self.depenses_mensuelle} €.\n"
                f"Son objectif est de {self.objectif} €, avec une duree d'epargne de {self.duree_epargne} ans.\n"
                f"Son versement mensuel est de {self.versement_mensuel_utilisateur} €."
                f"Sa capacité d'épargne est de {self._calcul_capacite_epargne()} €")

    def __repr__(self):
        return f"""
                Personne(
                \tnom={self.nom},
                \tage={self.age},
                \trevenu_annuel={self.revenu_annuel},
                \tloyer={self.loyer},
                \tdepenses_mensuelle={self.depenses_mensuelle},
                \tobjectif={self.objectif},
                \tduree_epargne={self.duree_epargne},
                \tversement_mensuel_utilisateur={self.versement_mensuel_utilisateur}
                \tcapacite_epargne={self._calcul_capacite_epargne()}
                )
                """

    def _calcul_capacite_epargne(self) -> float:
        return (self.revenu_annuel / 12) - self.loyer - self.depenses_mensuelle