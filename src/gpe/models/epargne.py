class Epargne:

    def __init__(self, nom: str, taux_interet: float, fiscalite: float, duree_min: int, versement_max: float = None):
        self.nom = nom
        self.taux_interet = taux_interet
        self.fiscalite = fiscalite
        self.duree_min = duree_min
        self.versement_max = versement_max

    def __repr__(self):
        return f"""
Epargne(
\tnom={self.nom},
\ttaux_interet={self.taux_interet},
\tfiscalite={self.fiscalite},
\tduree_min={self.duree_min},
\tversement_max={self.versement_max}
)
"""

    def __str__(self):
        versement_info = f"avec un versement maximum de {self.versement_max} €" if self.versement_max is not None else "sans limite de versement"
        return (f"Produit d'épargne '{self.nom}' avec un taux d'intérêt de {self.taux_interet}, "
                f"une fiscalité de {self.fiscalite}, une durée minimale de {self.duree_min} ans, "
                f"{versement_info}.")

if __name__ == '__main__':
    epargne_1 = Epargne(
        nom="Livret A",
        taux_interet=0.03,
        fiscalite=0.172,
        duree_min=0
    )

    print(str(epargne_1))
    print(repr(epargne_1))