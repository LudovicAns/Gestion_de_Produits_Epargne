import pandas as pd

class ResultatEpargne:

    def __init__(self, nom_produit_epargne: str, effort_mensuel: float, total_versement: float, versement_max_epargne:float, montant_net_final: float, objectif_atteint: bool, interet_brut: float, interet_net: float):
        self.nom_produit_epargne = nom_produit_epargne
        self.effort_mensuel = effort_mensuel
        self.total_versement = total_versement
        self.versement_max_epargne = versement_max_epargne
        self.montant_net_final = montant_net_final
        self.objectif_atteint = objectif_atteint
        self.interet_brut = interet_brut
        self.interet_net = interet_net

    def __str__(self):
        return (f"ResultatEpargne(\n"
                f"\tnom_produit_epargne={self.nom_produit_epargne},\n"
                f"\teffort_mensuel={self.effort_mensuel:.2f},\n"
                f"\ttotal_versement={self.total_versement:.2f},\n"
                f"\tversement_max_epargne={self.versement_max_epargne:.2f},\n"
                f"\tmontant_net_final={self.montant_net_final:.2f} €,\n"
                f"\tobjectif_atteint={self.objectif_atteint},\n"
                f"\tinteret_brut={self.interet_brut:.2f} €,\n"
                f"\tinteret_net={self.interet_net:.2f} €\n"
                f")")

    def afficher(self):
        print(f"{self.nom_produit_epargne:<40} "
              f"{self.effort_mensuel:>15.2f} % "
              f"{self.montant_net_final:>15.2f} € "
              f"{self.interet_brut:>15.2f} € "
              f"{self.interet_net:>15.2f} €"
              f"{self.total_versement:>15.2f} €"
              f"{'Aucun' if not self.versement_max_epargne else f'{self.versement_max_epargne:.2f} €':>15}")

    def to_dataframe(self):
        pd.DataFrame({
            "nom_produit_epargne": self.nom_produit_epargne,
            "effort_mensuel": self.effort_mensuel,
            "total_versement": self.total_versement,
            "versement_max_epargne": self.versement_max_epargne,
            "montant_net_final": self.montant_net_final,
            "objectif_atteint": self.objectif_atteint,
            "interet_brut": self.interet_brut,
            "interet_net": self.interet_net,
        })