import os
import logging
import pandas as pd
from typing import List, Union
from pathlib import Path
from dataclasses import dataclass

from src.gpe.models.personne import Personne
from src.gpe.models.epargne import Epargne
from src.gpe.models.resultat import ResultatEpargne
from src.gpe.utils import nettoyer_dataframe_personne, nettoyer_dataframe_epargne, calcul_interets_composes

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def import_personnes(fichier: str) -> List[Personne]:
    """
    Importe des données de personnes depuis un fichier et les convertit en objets Personne.

    Args:
        fichier (str): Chemin vers le fichier à importer (formats supportés: CSV, TXT, XLSX)

    Returns:
        List[Personne]: Liste d'objets Personne

    Raises:
        ValueError: Si le format du fichier n'est pas supporté ou si les données sont invalides
        FileNotFoundError: Si le fichier n'existe pas
    """
    if not os.path.exists(fichier):
        logger.error(f"Le fichier {fichier} n'existe pas")
        raise FileNotFoundError(f"Le fichier {fichier} n'existe pas")

    # Déterminer le format du fichier
    extension = Path(fichier).suffix.lower()

    try:
        # Charger les données selon le format
        if extension == '.csv':
            df = pd.read_csv(fichier)
        elif extension == '.txt':
            df = pd.read_csv(fichier, sep='\t')
        elif extension == '.xlsx':
            df = pd.read_excel(fichier)
        else:
            logger.error(f"Format de fichier non supporté: {extension}")
            raise ValueError(f"Format de fichier non supporté: {extension}. Utilisez CSV, TXT ou XLSX.")

        # Vérifier que les colonnes nécessaires sont présentes
        colonnes_requises = ['nom', 'age', 'revenu_annuel', 'loyer', 'depenses_mensuelles', 'objectif']
        colonnes_manquantes = [col for col in colonnes_requises if col not in df.columns]

        # Gérer les différentes orthographes possibles pour la durée
        if 'duree_epargne' not in df.columns and 'duree' not in df.columns and 'durée' not in df.columns:
            colonnes_manquantes.append('duree_epargne/duree/durée')

        if colonnes_manquantes:
            logger.error(f"Colonnes manquantes dans le fichier: {colonnes_manquantes}")
            raise ValueError(f"Colonnes manquantes dans le fichier: {colonnes_manquantes}")

        # Standardiser le nom de la colonne durée
        if 'durée' in df.columns:
            df = df.rename(columns={'durée': 'duree_epargne'})
        elif 'duree' in df.columns:
            df = df.rename(columns={'duree': 'duree_epargne'})

        # Nettoyer les données
        df_clean = nettoyer_dataframe_personne(df)

        # Convertir en objets Personne
        personnes = []
        for _, row in df_clean.iterrows():
            try:
                # Gérer le cas où versement_mensuel_utilisateur est absent
                versement = row.get('versement_mensuel_utilisateur', 0)
                if pd.isna(versement):
                    versement = 0

                personne = Personne(
                    nom=row['nom'],
                    age=row['age'],
                    revenu_annuel=row['revenu_annuel'],
                    loyer=row['loyer'],
                    depenses_mensuelles=row['depenses_mensuelles'],
                    objectif=row['objectif'],
                    duree_epargne=row['duree_epargne'],
                    versement_mensuel_utilisateur=versement
                )
                personnes.append(personne)
            except Exception as e:
                logger.warning(f"Impossible de créer une personne à partir de la ligne {row}: {str(e)}")

        logger.info(f"Import réussi: {len(personnes)} personnes importées depuis {fichier}")
        return personnes

    except Exception as e:
        logger.error(f"Erreur lors de l'import du fichier {fichier}: {str(e)}")
        raise

def import_epargnes(fichier: str) -> List[Epargne]:
    """
    Importe des données d'épargne depuis un fichier et les convertit en objets Epargne.

    Args:
        fichier (str): Chemin vers le fichier à importer (formats supportés: CSV, TXT, XLSX)

    Returns:
        List[Epargne]: Liste d'objets Epargne

    Raises:
        ValueError: Si le format du fichier n'est pas supporté ou si les données sont invalides
        FileNotFoundError: Si le fichier n'existe pas
    """
    if not os.path.exists(fichier):
        logger.error(f"Le fichier {fichier} n'existe pas")
        raise FileNotFoundError(f"Le fichier {fichier} n'existe pas")

    # Déterminer le format du fichier
    extension = Path(fichier).suffix.lower()

    try:
        # Charger les données selon le format
        if extension == '.csv':
            df = pd.read_csv(fichier)
        elif extension == '.txt':
            df = pd.read_csv(fichier, sep='\t')
        elif extension == '.xlsx':
            df = pd.read_excel(fichier)
        else:
            logger.error(f"Format de fichier non supporté: {extension}")
            raise ValueError(f"Format de fichier non supporté: {extension}. Utilisez CSV, TXT ou XLSX.")

        # Vérifier que les colonnes nécessaires sont présentes
        colonnes_requises = ['nom', 'taux_interet', 'fiscalite', 'duree_min']
        colonnes_manquantes = [col for col in colonnes_requises if col not in df.columns]

        if colonnes_manquantes:
            logger.error(f"Colonnes manquantes dans le fichier: {colonnes_manquantes}")
            raise ValueError(f"Colonnes manquantes dans le fichier: {colonnes_manquantes}")

        # Nettoyer les données
        df_clean = nettoyer_dataframe_epargne(df)

        # Convertir en objets Epargne
        epargnes = []
        for _, row in df_clean.iterrows():
            try:
                # Gérer le cas où versement_max est NaN
                versement_max = row.get('versement_max')
                if pd.isna(versement_max):
                    versement_max = None

                epargne = Epargne(
                    nom=row['nom'],
                    taux_interet=row['taux_interet'],
                    fiscalite=row['fiscalite'],
                    duree_min=row['duree_min'],
                    versement_max=versement_max
                )
                epargnes.append(epargne)
            except Exception as e:
                logger.warning(f"Impossible de créer une épargne à partir de la ligne {row}: {str(e)}")

        logger.info(f"Import réussi: {len(epargnes)} produits d'épargne importés depuis {fichier}")
        return epargnes

    except Exception as e:
        logger.error(f"Erreur lors de l'import du fichier {fichier}: {str(e)}")
        raise

def save_personnes(personnes: List[Personne], fichier: str) -> None:
    """
    Sauvegarde une liste de personnes dans un fichier.

    Args:
        personnes (List[Personne]): Liste d'objets Personne à sauvegarder
        fichier (str): Chemin vers le fichier de destination (formats supportés: CSV, TXT, XLSX)

    Raises:
        ValueError: Si le format du fichier n'est pas supporté
    """
    # Créer un DataFrame à partir des objets Personne
    data = []
    for p in personnes:
        data.append({
            'nom': p.nom,
            'age': p.age,
            'revenu_annuel': p.revenu_annuel,
            'loyer': p.loyer,
            'depenses_mensuelles': p.depenses_mensuelles,
            'objectif': p.objectif,
            'duree_epargne': p.duree_epargne,
            'versement_mensuel_utilisateur': p.versement_mensuel_utilisateur
        })

    df = pd.DataFrame(data)

    # Déterminer le format du fichier
    extension = Path(fichier).suffix.lower()

    try:
        # Sauvegarder selon le format
        if extension == '.csv':
            df.to_csv(fichier, index=False)
        elif extension == '.txt':
            df.to_csv(fichier, sep='\t', index=False)
        elif extension == '.xlsx':
            try:
                df.to_excel(fichier, index=False)
            except ImportError as e:
                logger.error(f"Impossible de sauvegarder au format Excel: {str(e)}")
                logger.info("Installation du package openpyxl requise pour le format Excel. Utilisation du format CSV par défaut.")
                # Sauvegarder en CSV à la place
                csv_path = Path(fichier).with_suffix('.csv')
                df.to_csv(csv_path, index=False)
                logger.info(f"Sauvegardé en CSV à la place: {csv_path}")
                return  # Sortir de la fonction après la sauvegarde alternative
        else:
            logger.error(f"Format de fichier non supporté: {extension}")
            raise ValueError(f"Format de fichier non supporté: {extension}. Utilisez CSV, TXT ou XLSX.")

        logger.info(f"Sauvegarde réussie: {len(personnes)} personnes sauvegardées dans {fichier}")

    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde dans le fichier {fichier}: {str(e)}")
        raise

def save_epargnes(epargnes: List[Epargne], fichier: str) -> None:
    """
    Sauvegarde une liste de produits d'épargne dans un fichier.

    Args:
        epargnes (List[Epargne]): Liste d'objets Epargne à sauvegarder
        fichier (str): Chemin vers le fichier de destination (formats supportés: CSV, TXT, XLSX)

    Raises:
        ValueError: Si le format du fichier n'est pas supporté
    """
    # Créer un DataFrame à partir des objets Epargne
    data = []
    for e in epargnes:
        data.append({
            'nom': e.nom,
            'taux_interet': e.taux_interet,
            'fiscalite': e.fiscalite,
            'duree_min': e.duree_min,
            'versement_max': e.versement_max
        })

    df = pd.DataFrame(data)

    # Déterminer le format du fichier
    extension = Path(fichier).suffix.lower()

    try:
        # Sauvegarder selon le format
        if extension == '.csv':
            df.to_csv(fichier, index=False)
        elif extension == '.txt':
            df.to_csv(fichier, sep='\t', index=False)
        elif extension == '.xlsx':
            try:
                df.to_excel(fichier, index=False)
            except ImportError as e:
                logger.error(f"Impossible de sauvegarder au format Excel: {str(e)}")
                logger.info("Installation du package openpyxl requise pour le format Excel. Utilisation du format CSV par défaut.")
                # Sauvegarder en CSV à la place
                csv_path = Path(fichier).with_suffix('.csv')
                df.to_csv(csv_path, index=False)
                logger.info(f"Sauvegardé en CSV à la place: {csv_path}")
                return  # Sortir de la fonction après la sauvegarde alternative
        else:
            logger.error(f"Format de fichier non supporté: {extension}")
            raise ValueError(f"Format de fichier non supporté: {extension}. Utilisez CSV, TXT ou XLSX.")

        logger.info(f"Sauvegarde réussie: {len(epargnes)} produits d'épargne sauvegardés dans {fichier}")

    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde dans le fichier {fichier}: {str(e)}")
        raise

def suggestion_epargne(personne: Personne, epargnes: List[Epargne], objectif: float, duree: int) -> List[ResultatEpargne]:
    # Calculer la capacité d'épargne mensuelle de la personne
    capacite_epargne_mensuelle = personne._calcul_capacite_epargne()

    # Liste pour stocker les résultats
    resultats = []

    # Pour chaque produit d'épargne
    for epargne in epargnes:
        # Vérifier si la durée d'investissement est suffisante
        if duree < epargne.duree_min:
            # Ignorer ce produit si la durée est insuffisante
            continue

        # Définir les scénarios d'effort (pourcentages de la capacité d'épargne)
        scenarios = [
            (personne.versement_mensuel_utilisateur, 0),  # L'effort saisi par l'utilisateur
            (0.25 * capacite_epargne_mensuelle, 25),      # 25% de la capacité
            (0.50 * capacite_epargne_mensuelle, 50),      # 50% de la capacité
            (0.75 * capacite_epargne_mensuelle, 75),      # 75% de la capacité
            (1.00 * capacite_epargne_mensuelle, 100)      # 100% de la capacité
        ]

        # Pour chaque scénario
        for versement_mensuel, pourcentage in scenarios:

            # Calculer le versement annuel
            versement_annuel = versement_mensuel * 12

            # Vérifier si le versement respecte le plafond éventuel du produit
            if epargne.versement_max is not None and versement_annuel * duree > epargne.versement_max:
                # Ignorer ce scénario si le plafond est dépassé
                continue

            # Versement total
            versement_total = versement_annuel * duree

            # Calculer le capital brut avec intérêts
            capital_brut = calcul_interets_composes(versement_annuel, epargne.taux_interet, duree)

            # Intérêt total brut
            interet_total_brut = capital_brut - versement_total

            # Intérêt total net
            interet_total_net = interet_total_brut * (1 - epargne.fiscalite)

            # Capital net
            capital_net = interet_total_net + versement_total

            resultats.append(ResultatEpargne(
                nom_produit_epargne=epargne.nom,
                effort_mensuel=pourcentage,
                total_versement=versement_total,
                montant_net_final=capital_net,
                objectif_atteint=capital_net >= objectif,
                interet_brut=interet_total_brut,
                interet_net=interet_total_net
            ))


    return resultats
