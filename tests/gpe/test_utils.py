import unittest
import pandas as pd
import numpy as np
from src.gpe.utils import (
    calcul_interets_composes, 
    nettoyer_valeur_manquante, 
    convertir_en_float, 
    convertir_en_int,
    nettoyer_dataframe_epargne,
    nettoyer_dataframe_personne
)

class TestCalculInteretsComposes(unittest.TestCase):
    """Tests unitaires pour la fonction calcul_interets_composes."""

    def test_calcul_simple(self):
        """Test avec un exemple simple: 1000€/an, 3% d'intérêt, sur 5 ans."""
        resultat = calcul_interets_composes(1000, 0.03, 5)
        self.assertAlmostEqual(resultat, 5468.41, places=2)

    def test_taux_eleve(self):
        """Test avec un taux d'intérêt plus élevé: 1000€/an, 5% d'intérêt, sur 10 ans."""
        resultat = calcul_interets_composes(1000, 0.05, 10)
        self.assertAlmostEqual(resultat, 13206.79, places=2)

    def test_versement_eleve(self):
        """Test avec un versement annuel plus élevé: 5000€/an, 2% d'intérêt, sur 3 ans."""
        resultat = calcul_interets_composes(5000, 0.02, 3)
        self.assertAlmostEqual(resultat, 15608.04, places=2)

    def test_verification_manuelle(self):
        """
        Test avec une vérification manuelle:
        Pour 1000€/an, 10% d'intérêt, sur 2 ans:
        Année 1: (0 + 1000) * 1.1 = 1100
        Année 2: (1100 + 1000) * 1.1 = 2310
        """
        resultat = calcul_interets_composes(1000, 0.1, 2)
        self.assertEqual(resultat, 2310.0)

    def test_duree_zero(self):
        """Test avec une durée de 0 an (devrait retourner 0)."""
        resultat = calcul_interets_composes(1000, 0.05, 0)
        self.assertEqual(resultat, 0)

    def test_versement_zero(self):
        """Test avec un versement de 0€ (devrait retourner 0 peu importe la durée)."""
        resultat = calcul_interets_composes(0, 0.05, 5)
        self.assertEqual(resultat, 0)

    def test_taux_zero(self):
        """Test avec un taux d'intérêt de 0% (devrait retourner la somme des versements)."""
        resultat = calcul_interets_composes(1000, 0, 5)
        self.assertEqual(resultat, 5000)


class TestNettoyageValeurs(unittest.TestCase):
    """Tests unitaires pour les fonctions de nettoyage de valeurs."""

    def test_nettoyer_valeur_manquante(self):
        """Test de la fonction nettoyer_valeur_manquante."""
        # Test avec None
        self.assertIsNone(nettoyer_valeur_manquante(None))
        # Test avec NaN
        self.assertIsNone(nettoyer_valeur_manquante(np.nan))
        # Test avec "None"
        self.assertIsNone(nettoyer_valeur_manquante("None"))
        # Test avec chaîne vide
        self.assertIsNone(nettoyer_valeur_manquante(""))
        # Test avec valeur normale
        self.assertEqual(nettoyer_valeur_manquante(42), 42)
        self.assertEqual(nettoyer_valeur_manquante("test"), "test")

    def test_convertir_en_float(self):
        """Test de la fonction convertir_en_float."""
        # Test avec None
        self.assertIsNone(convertir_en_float(None))
        # Test avec NaN
        self.assertIsNone(convertir_en_float(np.nan))
        # Test avec "None"
        self.assertIsNone(convertir_en_float("None"))
        # Test avec chaîne vide
        self.assertIsNone(convertir_en_float(""))
        # Test avec valeur normale
        self.assertEqual(convertir_en_float(42), 42.0)
        self.assertEqual(convertir_en_float("42"), 42.0)
        self.assertEqual(convertir_en_float("42.5"), 42.5)
        # Test avec valeur invalide
        with self.assertRaises(ValueError):
            convertir_en_float("abc")

    def test_convertir_en_int(self):
        """Test de la fonction convertir_en_int."""
        # Test avec None
        self.assertIsNone(convertir_en_int(None))
        # Test avec NaN
        self.assertIsNone(convertir_en_int(np.nan))
        # Test avec "None"
        self.assertIsNone(convertir_en_int("None"))
        # Test avec chaîne vide
        self.assertIsNone(convertir_en_int(""))
        # Test avec valeur normale
        self.assertEqual(convertir_en_int(42), 42)
        self.assertEqual(convertir_en_int("42"), 42)
        self.assertEqual(convertir_en_int(42.5), 42)
        self.assertEqual(convertir_en_int("42.5"), 42)
        # Test avec valeur invalide
        with self.assertRaises(ValueError):
            convertir_en_int("abc")


class TestNettoyageDataFrames(unittest.TestCase):
    """Tests unitaires pour les fonctions de nettoyage de DataFrames."""

    def test_nettoyer_dataframe_epargne(self):
        """Test de la fonction nettoyer_dataframe_epargne."""
        # Créer un DataFrame de test
        df = pd.DataFrame({
            'nom': ['Test1', 'Test2', 'Test3'],
            'taux_interet': [0.02, "0.03", "None"],
            'fiscalite': [0.0, "0.3", np.nan],
            'duree_min': [0, "5", None],
            'versement_max': [10000, "20000", "None"]
        })

        # Nettoyer le DataFrame
        df_clean = nettoyer_dataframe_epargne(df)

        # Vérifier les types des colonnes
        self.assertEqual(df_clean['taux_interet'].dtype, float)
        self.assertEqual(df_clean['fiscalite'].dtype, float)
        # Pour duree_min, vérifier que c'est soit int soit Int64 (si contient des None)
        self.assertTrue(df_clean['duree_min'].dtype == int or str(df_clean['duree_min'].dtype) == 'Int64')
        self.assertEqual(df_clean['versement_max'].dtype, float)

        # Vérifier les valeurs
        self.assertEqual(df_clean['taux_interet'][0], 0.02)
        self.assertEqual(df_clean['taux_interet'][1], 0.03)
        self.assertTrue(pd.isna(df_clean['taux_interet'][2]))

        self.assertEqual(df_clean['fiscalite'][0], 0.0)
        self.assertEqual(df_clean['fiscalite'][1], 0.3)
        self.assertTrue(pd.isna(df_clean['fiscalite'][2]))

        self.assertEqual(df_clean['duree_min'][0], 0)
        self.assertEqual(df_clean['duree_min'][1], 5)
        self.assertTrue(pd.isna(df_clean['duree_min'][2]))

        self.assertEqual(df_clean['versement_max'][0], 10000.0)
        self.assertEqual(df_clean['versement_max'][1], 20000.0)
        self.assertTrue(pd.isna(df_clean['versement_max'][2]))

        # Test avec un DataFrame sans les colonnes requises
        df_invalide = pd.DataFrame({'nom': ['Test']})
        with self.assertRaises(ValueError):
            nettoyer_dataframe_epargne(df_invalide)

    def test_nettoyer_dataframe_personne(self):
        """Test de la fonction nettoyer_dataframe_personne."""
        # Créer un DataFrame de test
        df = pd.DataFrame({
            'nom': ['Test1', 'Test2', 'Test3'],
            'age': [25, "30", None],
            'revenu_annuel': [30000, "40000", np.nan],
            'loyer': [800, "900", "None"],
            'depenses_mensuelles': [500, "600", ""],
            'versement_mensuel_utilisateur': [200, "", None]
        })

        # Nettoyer le DataFrame
        df_clean = nettoyer_dataframe_personne(df)

        # Vérifier les types des colonnes
        # Pour age, vérifier que c'est soit int soit Int64 (si contient des None)
        self.assertTrue(df_clean['age'].dtype == int or str(df_clean['age'].dtype) == 'Int64')
        self.assertEqual(df_clean['revenu_annuel'].dtype, float)
        self.assertEqual(df_clean['loyer'].dtype, float)
        self.assertEqual(df_clean['depenses_mensuelles'].dtype, float)
        self.assertEqual(df_clean['versement_mensuel_utilisateur'].dtype, float)

        # Vérifier les valeurs
        self.assertEqual(df_clean['age'][0], 25)
        self.assertEqual(df_clean['age'][1], 30)
        self.assertTrue(pd.isna(df_clean['age'][2]))

        self.assertEqual(df_clean['revenu_annuel'][0], 30000.0)
        self.assertEqual(df_clean['revenu_annuel'][1], 40000.0)
        self.assertTrue(pd.isna(df_clean['revenu_annuel'][2]))

        self.assertEqual(df_clean['loyer'][0], 800.0)
        self.assertEqual(df_clean['loyer'][1], 900.0)
        self.assertTrue(pd.isna(df_clean['loyer'][2]))

        self.assertEqual(df_clean['depenses_mensuelles'][0], 500.0)
        self.assertEqual(df_clean['depenses_mensuelles'][1], 600.0)
        self.assertTrue(pd.isna(df_clean['depenses_mensuelles'][2]))

        self.assertEqual(df_clean['versement_mensuel_utilisateur'][0], 200.0)
        self.assertTrue(pd.isna(df_clean['versement_mensuel_utilisateur'][1]))
        self.assertTrue(pd.isna(df_clean['versement_mensuel_utilisateur'][2]))

        # Test avec un DataFrame sans les colonnes requises
        df_invalide = pd.DataFrame({'nom': ['Test']})
        with self.assertRaises(ValueError):
            nettoyer_dataframe_personne(df_invalide)


if __name__ == '__main__':
    unittest.main()
