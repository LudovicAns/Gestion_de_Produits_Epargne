import unittest
import os
import pandas as pd
from pathlib import Path
from tempfile import NamedTemporaryFile

from src.gpe.core import import_personnes, import_epargnes, save_personnes, save_epargnes
from src.gpe.models.personne import Personne
from src.gpe.models.epargne import Epargne

class TestCore(unittest.TestCase):

    def setUp(self):
        # Obtenir le chemin absolu du répertoire racine du projet
        project_root = Path(__file__).parent.parent.parent
        data_dir = project_root / "src" / "gpe" / "data"

        # Définir les chemins absolus pour les fichiers de test
        self.personnes_csv = str(data_dir / "personnes.csv")
        self.epargnes_csv = str(data_dir / "epargnes.csv")
        self.personnes_txt = str(data_dir / "personnes.txt")
        self.epargnes_txt = str(data_dir / "epargnes.txt")

    def test_import_personnes_csv(self):
        """Test l'import de personnes depuis un fichier CSV."""
        personnes = import_personnes(self.personnes_csv)
        self.assertIsInstance(personnes, list)
        self.assertTrue(len(personnes) > 0)
        self.assertIsInstance(personnes[0], Personne)

        # Vérifier quelques attributs
        self.assertEqual(personnes[0].nom, "Alice")
        self.assertEqual(personnes[0].age, 22)
        self.assertEqual(personnes[0].revenu_annuel, 21000)

    def test_import_personnes_txt(self):
        """Test l'import de personnes depuis un fichier TXT."""
        personnes = import_personnes(self.personnes_txt)
        self.assertIsInstance(personnes, list)
        self.assertTrue(len(personnes) > 0)
        self.assertIsInstance(personnes[0], Personne)

        # Vérifier quelques attributs
        self.assertEqual(personnes[0].nom, "Alice")
        self.assertEqual(personnes[0].age, 22)
        self.assertEqual(personnes[0].revenu_annuel, 21000)

    def test_import_epargnes_csv(self):
        """Test l'import d'épargnes depuis un fichier CSV."""
        epargnes = import_epargnes(self.epargnes_csv)
        self.assertIsInstance(epargnes, list)
        self.assertTrue(len(epargnes) > 0)
        self.assertIsInstance(epargnes[0], Epargne)

        # Vérifier quelques attributs
        self.assertEqual(epargnes[0].nom, "Livret A")
        self.assertEqual(epargnes[0].taux_interet, 0.024)
        self.assertEqual(epargnes[0].fiscalite, 0.0)

    def test_import_epargnes_txt(self):
        """Test l'import d'épargnes depuis un fichier TXT."""
        epargnes = import_epargnes(self.epargnes_txt)
        self.assertIsInstance(epargnes, list)
        self.assertTrue(len(epargnes) > 0)
        self.assertIsInstance(epargnes[0], Epargne)

        # Vérifier quelques attributs
        self.assertEqual(epargnes[0].nom, "Livret A")
        self.assertEqual(epargnes[0].taux_interet, 0.024)
        self.assertEqual(epargnes[0].fiscalite, 0.0)

    def test_save_and_import_personnes(self):
        """Test la sauvegarde et l'import de personnes."""
        # Créer quelques personnes
        personnes = [
            Personne("Test1", 30, 40000, 800, 600, 100000, 10, 500),
            Personne("Test2", 40, 50000, 1000, 800, 200000, 15, 700)
        ]

        # Tester les différents formats
        for extension in ['.csv', '.txt']:  # Exclure '.xlsx' pour éviter les problèmes de dépendance
            with NamedTemporaryFile(suffix=extension, delete=False) as temp:
                temp_path = temp.name

            try:
                # Sauvegarder les personnes
                save_personnes(personnes, temp_path)

                # Vérifier que le fichier existe
                self.assertTrue(os.path.exists(temp_path))

                # Importer les personnes
                imported_personnes = import_personnes(temp_path)

                # Vérifier que les données sont correctes
                self.assertEqual(len(imported_personnes), 2)
                self.assertEqual(imported_personnes[0].nom, "Test1")
                self.assertEqual(imported_personnes[1].nom, "Test2")
            finally:
                # Nettoyer
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    def test_save_and_import_epargnes(self):
        """Test la sauvegarde et l'import d'épargnes."""
        # Créer quelques épargnes
        epargnes = [
            Epargne("TestEpargne1", 0.03, 0.15, 5, 10000),
            Epargne("TestEpargne2", 0.04, 0.20, 8, None)
        ]

        # Tester les différents formats
        for extension in ['.csv', '.txt']:  # Exclure '.xlsx' pour éviter les problèmes de dépendance
            with NamedTemporaryFile(suffix=extension, delete=False) as temp:
                temp_path = temp.name

            try:
                # Sauvegarder les épargnes
                save_epargnes(epargnes, temp_path)

                # Vérifier que le fichier existe
                self.assertTrue(os.path.exists(temp_path))

                # Importer les épargnes
                imported_epargnes = import_epargnes(temp_path)

                # Vérifier que les données sont correctes
                self.assertEqual(len(imported_epargnes), 2)
                self.assertEqual(imported_epargnes[0].nom, "TestEpargne1")
                self.assertEqual(imported_epargnes[1].nom, "TestEpargne2")
                self.assertEqual(imported_epargnes[0].versement_max, 10000)
                self.assertIsNone(imported_epargnes[1].versement_max)
            finally:
                # Nettoyer
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    def test_format_non_supporte(self):
        """Test qu'une erreur est levée pour un format non supporté."""
        with NamedTemporaryFile(suffix='.json', delete=False) as temp:
            temp_path = temp.name

        try:
            # Créer quelques personnes
            personnes = [Personne("Test", 30, 40000, 800, 600, 100000, 10, 500)]

            # Vérifier que l'erreur est levée
            with self.assertRaises(ValueError):
                save_personnes(personnes, temp_path)

            # Vérifier que l'erreur est levée
            with self.assertRaises(ValueError):
                import_personnes(temp_path)
        finally:
            # Nettoyer
            if os.path.exists(temp_path):
                os.remove(temp_path)

if __name__ == '__main__':
    unittest.main()
