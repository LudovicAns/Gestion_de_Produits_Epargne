import unittest
from src.gpe.models.personne import Personne

class TestPersonne(unittest.TestCase):
    """Tests unitaires pour la classe Personne."""

    def setUp(self):
        """Initialisation des objets Personne pour les tests."""
        # Personne avec tous les paramètres
        self.personne_complete = Personne(
            nom="Jean Dupont",
            age=30,
            revenu_annuel=36000,
            loyer=800,
            depenses_mensuelle=1000,
            objectif=50000,
            duree_epargne=10,
            versement_mensuel_utilisateur=500
        )

        # Personne sans versement mensuel utilisateur (valeur par défaut)
        self.personne_sans_versement = Personne(
            nom="Marie Martin",
            age=25,
            revenu_annuel=30000,
            loyer=700,
            depenses_mensuelle=800,
            objectif=40000,
            duree_epargne=8
        )

    def test_initialisation(self):
        """Test l'initialisation correcte des attributs de la classe Personne."""
        # Test avec tous les paramètres
        self.assertEqual(self.personne_complete.nom, "Jean Dupont")
        self.assertEqual(self.personne_complete.age, 30)
        self.assertEqual(self.personne_complete.revenu_annuel, 36000)
        self.assertEqual(self.personne_complete.loyer, 800)
        self.assertEqual(self.personne_complete.depenses_mensuelle, 1000)
        self.assertEqual(self.personne_complete.objectif, 50000)
        self.assertEqual(self.personne_complete.duree_epargne, 10)
        self.assertEqual(self.personne_complete.versement_mensuel_utilisateur, 500)

        # Test sans versement mensuel utilisateur
        self.assertEqual(self.personne_sans_versement.nom, "Marie Martin")
        self.assertEqual(self.personne_sans_versement.age, 25)
        self.assertEqual(self.personne_sans_versement.revenu_annuel, 30000)
        self.assertEqual(self.personne_sans_versement.loyer, 700)
        self.assertEqual(self.personne_sans_versement.depenses_mensuelle, 800)
        self.assertEqual(self.personne_sans_versement.objectif, 40000)
        self.assertEqual(self.personne_sans_versement.duree_epargne, 8)
        self.assertEqual(self.personne_sans_versement.versement_mensuel_utilisateur, 0)

    def test_calcul_capacite_epargne(self):
        """Test la méthode _calcul_capacite_epargne de la classe Personne."""
        # Calcul pour la première personne: (36000 / 12) - 800 - 1000 = 3000 - 800 - 1000 = 1200
        self.assertEqual(self.personne_complete._calcul_capacite_epargne(), 1200)

        # Calcul pour la deuxième personne: (30000 / 12) - 700 - 800 = 2500 - 700 - 800 = 1000
        self.assertEqual(self.personne_sans_versement._calcul_capacite_epargne(), 1000)

    def test_str(self):
        """Test la méthode __str__ de la classe Personne."""
        # Vérifier que __str__ contient les informations essentielles
        str_personne = str(self.personne_complete)
        self.assertIn("Jean Dupont", str_personne)
        self.assertIn("30 ans", str_personne)
        self.assertIn("36000 €", str_personne)
        self.assertIn("loyer de 800 €", str_personne)
        self.assertIn("depense mensuelle de 1000 €", str_personne)
        self.assertIn("objectif est de 50000 €", str_personne)
        self.assertIn("duree d'epargne de 10 ans", str_personne)
        self.assertIn("versement mensuel est de 500 €", str_personne)
        self.assertIn("capacité d'épargne est de 1200.0 €", str_personne)

    def test_repr(self):
        """Test la méthode __repr__ de la classe Personne."""
        # Vérifier que __repr__ contient les informations essentielles
        repr_personne = repr(self.personne_complete)
        self.assertIn("nom=Jean Dupont", repr_personne)
        self.assertIn("age=30", repr_personne)
        self.assertIn("revenu_annuel=36000", repr_personne)
        self.assertIn("loyer=800", repr_personne)
        self.assertIn("depenses_mensuelle=1000", repr_personne)
        self.assertIn("objectif=50000", repr_personne)
        self.assertIn("duree_epargne=10", repr_personne)
        self.assertIn("versement_mensuel_utilisateur=500", repr_personne)
        self.assertIn("capacite_epargne=1200", repr_personne)

if __name__ == '__main__':
    unittest.main()
