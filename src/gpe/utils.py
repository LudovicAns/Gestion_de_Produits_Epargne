import pandas as pd
from typing import Union, List, Dict, Any


def calcul_interets_composes(versement_annuel: float, taux_annuel: float, duree_annees: int) -> float:
    """
    Calcule le montant accumulé par un placement à intérêts composés.

    La formule utilisée est: montant(n+1) = (montant(n) + versement_annuel) * (1 + taux_annuel)

    Args:
        versement_annuel (float): Montant versé chaque année
        taux_annuel (float): Taux d'intérêt annuel (ex: 0.03 pour 3%)
        duree_annees (int): Durée du placement en années

    Returns:
        float: Montant total accumulé après la durée spécifiée
    """
    montant = 0

    for _ in range(duree_annees):
        montant = (montant + versement_annuel) * (1 + taux_annuel)

    return montant


def nettoyer_valeur_manquante(valeur: Any) -> Any:
    """
    Nettoie les valeurs manquantes (NaN, None, "None") en les remplaçant par None.

    Args:
        valeur: La valeur à nettoyer

    Returns:
        La valeur nettoyée ou None si c'est une valeur manquante
    """
    if pd.isna(valeur) or valeur == "None" or valeur == "" or valeur is None:
        return None
    return valeur


def convertir_en_float(valeur: Any) -> Union[float, None]:
    """
    Convertit une valeur en float.

    Args:
        valeur: La valeur à convertir

    Returns:
        float: La valeur convertie en float
        None: Si la valeur est None ou ne peut pas être convertie

    Raises:
        ValueError: Si la valeur ne peut pas être convertie en float
    """
    valeur_nettoyee = nettoyer_valeur_manquante(valeur)
    if valeur_nettoyee is None:
        return None

    try:
        return float(valeur_nettoyee)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Impossible de convertir '{valeur}' en float: {str(e)}")


def convertir_en_int(valeur: Any) -> Union[int, None]:
    """
    Convertit une valeur en int.

    Args:
        valeur: La valeur à convertir

    Returns:
        int: La valeur convertie en int
        None: Si la valeur est None ou ne peut pas être convertie

    Raises:
        ValueError: Si la valeur ne peut pas être convertie en int
    """
    valeur_nettoyee = nettoyer_valeur_manquante(valeur)
    if valeur_nettoyee is None:
        return None

    try:
        return int(float(valeur_nettoyee))
    except (ValueError, TypeError) as e:
        raise ValueError(f"Impossible de convertir '{valeur}' en int: {str(e)}")


def nettoyer_dataframe_epargne(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie un DataFrame contenant des données d'épargne.

    Args:
        df: Le DataFrame à nettoyer

    Returns:
        pd.DataFrame: Le DataFrame nettoyé

    Raises:
        ValueError: Si le DataFrame ne contient pas les colonnes attendues
    """
    # Vérifier que les colonnes requises sont présentes
    colonnes_requises = ['taux_interet', 'fiscalite', 'duree_min', 'versement_max']
    colonnes_manquantes = [col for col in colonnes_requises if col not in df.columns]
    if colonnes_manquantes:
        raise ValueError(f"Colonnes manquantes dans le DataFrame: {colonnes_manquantes}")

    # Créer une copie pour éviter de modifier le DataFrame original
    df_clean = df.copy()

    # Nettoyer les valeurs manquantes
    for col in df_clean.columns:
        df_clean[col] = df_clean[col].apply(nettoyer_valeur_manquante)

    # Convertir les colonnes en float
    for col in ['taux_interet', 'fiscalite', 'versement_max']:
        df_clean[col] = df_clean[col].apply(lambda x: convertir_en_float(x))

    # Convertir les colonnes en int
    # Utiliser pd.Int64Dtype() pour gérer les valeurs None dans les colonnes entières
    df_clean['duree_min'] = df_clean['duree_min'].apply(lambda x: convertir_en_int(x))
    if df_clean['duree_min'].isna().any():
        # Si la colonne contient des None, utiliser le type Int64 de pandas
        df_clean['duree_min'] = df_clean['duree_min'].astype('Int64')
    else:
        # Sinon, utiliser le type int standard
        df_clean['duree_min'] = df_clean['duree_min'].astype(int)

    return df_clean


def nettoyer_dataframe_personne(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie un DataFrame contenant des données de personnes.

    Args:
        df: Le DataFrame à nettoyer

    Returns:
        pd.DataFrame: Le DataFrame nettoyé

    Raises:
        ValueError: Si le DataFrame ne contient pas les colonnes attendues
    """
    # Vérifier que les colonnes requises sont présentes
    colonnes_requises = ['age', 'revenu_annuel', 'loyer', 'depenses_mensuelles']
    colonnes_manquantes = [col for col in colonnes_requises if col not in df.columns]
    if colonnes_manquantes:
        raise ValueError(f"Colonnes manquantes dans le DataFrame: {colonnes_manquantes}")

    # Créer une copie pour éviter de modifier le DataFrame original
    df_clean = df.copy()

    # Nettoyer les valeurs manquantes
    for col in df_clean.columns:
        df_clean[col] = df_clean[col].apply(nettoyer_valeur_manquante)

    # Convertir les colonnes en float
    for col in ['revenu_annuel', 'loyer', 'depenses_mensuelles', 'versement_mensuel_utilisateur']:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].apply(lambda x: convertir_en_float(x))

    # Convertir les colonnes en int
    df_clean['age'] = df_clean['age'].apply(lambda x: convertir_en_int(x))
    if df_clean['age'].isna().any():
        # Si la colonne contient des None, utiliser le type Int64 de pandas
        df_clean['age'] = df_clean['age'].astype('Int64')
    else:
        # Sinon, utiliser le type int standard
        df_clean['age'] = df_clean['age'].astype(int)

    return df_clean
