import unittest
from src.gpe.utils import calcul_interets_composes

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

if __name__ == '__main__':
    unittest.main()
