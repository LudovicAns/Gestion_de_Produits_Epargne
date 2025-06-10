import unittest
from src.gpe.models.epargne import Epargne

class TestEpargne(unittest.TestCase):
    """Tests unitaires pour la classe Epargne."""

    def setUp(self):
        """Initialisation des objets Epargne pour les tests."""
        # Epargne avec tous les paramètres
        self.epargne_complete = Epargne(
            nom="Livret A",
            taux_interet=0.03,
            fiscalite=0.172,
            duree_min=0,
            versement_max=22950
        )

        # Epargne sans versement maximum
        self.epargne_sans_max = Epargne(
            nom="PEL",
            taux_interet=0.02,
            fiscalite=0.172,
            duree_min=4
        )

    def test_initialisation(self):
        """Test l'initialisation correcte des attributs de la classe Epargne."""
        # Test avec tous les paramètres
        self.assertEqual(self.epargne_complete.nom, "Livret A")
        self.assertEqual(self.epargne_complete.taux_interet, 0.03)
        self.assertEqual(self.epargne_complete.fiscalite, 0.172)
        self.assertEqual(self.epargne_complete.duree_min, 0)
        self.assertEqual(self.epargne_complete.versement_max, 22950)

        # Test sans versement maximum
        self.assertEqual(self.epargne_sans_max.nom, "PEL")
        self.assertEqual(self.epargne_sans_max.taux_interet, 0.02)
        self.assertEqual(self.epargne_sans_max.fiscalite, 0.172)
        self.assertEqual(self.epargne_sans_max.duree_min, 4)
        self.assertIsNone(self.epargne_sans_max.versement_max)

    def test_str(self):
        """Test la méthode __str__ de la classe Epargne."""
        # Test avec versement maximum
        expected_str_complete = "Produit d'épargne 'Livret A' avec un taux d'intérêt de 0.03, une fiscalité de 0.172, une durée minimale de 0 ans, avec un versement maximum de 22950 €."
        self.assertEqual(str(self.epargne_complete), expected_str_complete)

        # Test sans versement maximum
        expected_str_sans_max = "Produit d'épargne 'PEL' avec un taux d'intérêt de 0.02, une fiscalité de 0.172, une durée minimale de 4 ans, sans limite de versement."
        self.assertEqual(str(self.epargne_sans_max), expected_str_sans_max)

    def test_repr(self):
        """Test la méthode __repr__ de la classe Epargne."""
        # Vérifier que __repr__ contient les informations essentielles
        repr_complete = repr(self.epargne_complete)
        self.assertIn("nom=Livret A", repr_complete)
        self.assertIn("taux_interet=0.03", repr_complete)
        self.assertIn("fiscalite=0.172", repr_complete)
        self.assertIn("duree_min=0", repr_complete)
        self.assertIn("versement_max=22950", repr_complete)

        repr_sans_max = repr(self.epargne_sans_max)
        self.assertIn("nom=PEL", repr_sans_max)
        self.assertIn("taux_interet=0.02", repr_sans_max)
        self.assertIn("fiscalite=0.172", repr_sans_max)
        self.assertIn("duree_min=4", repr_sans_max)
        self.assertIn("versement_max=None", repr_sans_max)

if __name__ == '__main__':
    unittest.main()
