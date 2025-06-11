from src.gpe.models.epargne import Epargne

epargne_sans_versement_max = Epargne(
    nom="Livret A",
    taux_interet=0.03,
    fiscalite=0.172,
    duree_min=0
)

epargne_avec_versement_max = Epargne(
    nom="Livret A",
    taux_interet=0.03,
    fiscalite=0.172,
    duree_min=0,
    versement_max=100000.00
)

# todo:
#  - Tester le constructeur
#  - Tester la sortie __str__
#  - Tester la sortie __repr__