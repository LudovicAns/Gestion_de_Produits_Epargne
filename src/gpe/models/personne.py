class Personne:

    def __init__(self, nom: str, age: int, revenu_annuel: float, loyer: float, depenses_mensuelles: float, objectif: float, duree_epargne: int, versement_mensuel_utilisateur: float = 0):
        self.nom = nom
        self.age = age
        self.revenu_annuel = revenu_annuel
        self.loyer = loyer
        self.depenses_mensuelles = depenses_mensuelles
        self.objectif = objectif
        self.duree_epargne = duree_epargne
        self.versement_mensuel_utilisateur = versement_mensuel_utilisateur

    def __str__(self):
        return (f"{self.nom} {self.age} ans, a un revenu annuel de {self.revenu_annuel} €.\n"
                f"Paye un loyer de {self.loyer} € par mois, et a une depense mensuelle de {self.depenses_mensuelles} €.\n"
                f"Son objectif est de {self.objectif} €, avec une duree d'epargne de {self.duree_epargne} ans.\n"
                f"Son versement mensuel est de {self.versement_mensuel_utilisateur} €."
                f"Sa capacité d'épargne est de {self._calcul_capacite_epargne():.2f} €")

    def __repr__(self):
        return f"""
Personne(
\tnom={self.nom},
\tage={self.age},
\trevenu_annuel={self.revenu_annuel},
\tloyer={self.loyer},
\tdepenses_mensuelles={self.depenses_mensuelles},
\tobjectif={self.objectif},
\tduree_epargne={self.duree_epargne},
\tversement_mensuel_utilisateur={self.versement_mensuel_utilisateur}
\tcapacite_epargne={self._calcul_capacite_epargne():.2f}
)
"""

    def _calcul_capacite_epargne(self) -> float:
        return (self.revenu_annuel / 12) - self.loyer - self.depenses_mensuelles


if __name__ == '__main__':
    personne_1 = Personne(
        nom="Jacques",
        age=25,
        revenu_annuel=26000,
        loyer=600,
        depenses_mensuelles=300,
        objectif=1000,
        duree_epargne=10,
        versement_mensuel_utilisateur=500
    )

    print(str(personne_1))
    print(repr(personne_1))