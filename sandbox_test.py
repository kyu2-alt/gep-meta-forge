import unittest
from forge import GEPMetaForge

class TestGEPForgeSandbox(unittest.TestCase):
    def setUp(self):
        self.forge = GEPMetaForge()

    def test_evolver_version(self):
        self.assertEqual(self.forge.evolver_version, "1.89.17", "Must comply with EvoMap GEP envelope standard.")

    def test_mutation_engine(self):
        a = {"id": "test_1", "genome": "pass", "fitness_score": 0.5}
        b = {"id": "test_2", "genome": "pass", "fitness_score": 0.6}
        child = self.forge.mutate(a, b)
        self.assertIn("test_1", child["name"])
        self.assertIn("test_2", child["name"])
        self.assertTrue(child["fitness_expected"] > 0.6)

if __name__ == '__main__':
    unittest.main()
