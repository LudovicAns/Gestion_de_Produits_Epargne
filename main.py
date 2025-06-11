import sys
from pathlib import Path

from src.gpe.core import import_personnes, import_epargnes, suggestion_epargne

def main():
    # Définir les chemins des fichiers
    current_dir = Path(__file__).parent
    personnes_csv = current_dir / "src" / "gpe" / "data" / "personnes.csv"
    epargnes_csv = current_dir / "src" / "gpe" / "data" / "epargnes.csv"

    # Vérifier que les fichiers existent
    if not personnes_csv.exists():
        print(f"Erreur: Le fichier {personnes_csv} n'existe pas.")
        sys.exit(1)
    if not epargnes_csv.exists():
        print(f"Erreur: Le fichier {epargnes_csv} n'existe pas.")
        sys.exit(1)

    # Charger les données
    try:
        personnes = import_personnes(str(personnes_csv))
        epargnes = import_epargnes(str(epargnes_csv))
    except Exception as e:
        print(f"Erreur lors du chargement des données: {e}")
        sys.exit(1)

    print(f"Chargement réussi: {len(personnes)} personnes et {len(epargnes)} produits d'épargne.")

    # Pour chaque personne, suggérer des plans d'épargne
    for personne in personnes:
        print("\n" + "="*120)
        print(f"Suggestions d'épargne pour {personne.nom}:")
        print(f"Âge: {personne.age} ans")
        print(f"Revenu annuel: {personne.revenu_annuel:.2f} €")
        print(f"Capacité d'épargne mensuelle: {personne._calcul_capacite_epargne():.2f} €")
        print(f"Objectif: {personne.objectif:.2f} €")
        print(f"Durée d'épargne: {personne.duree_epargne} ans")
        print("-"*120)

        # Appeler la fonction de suggestion d'épargne
        resultats = suggestion_epargne(
            personne=personne,
            epargnes=epargnes,
            objectif=personne.objectif,
            duree=personne.duree_epargne
        )

        if not resultats:
            print("Aucune suggestion d'épargne disponible pour cette personne.")
            continue

        resultats = [r for r in resultats if r.objectif_atteint]
        # Trier les résultats par capital final décroissant
        resultats_tries = sorted(resultats, key=lambda r: r.montant_net_final, reverse=True)

        print(f"{'Produit':<40} {'Effort mensuel':>15} {'Capital final':>15} {'Intérêts bruts':>15} {'Intérêts nets':>15} {'Versement total':>20}")
        print("-" * 120)
        for resultat in resultats_tries:
            resultat.afficher()

if __name__ == "__main__":
    main()
