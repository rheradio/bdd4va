import unittest
import glob
import os
from random import randint

# Importing bdd4va from a relative path
import sys
sys.path.append("..")
from bdd4va.bdd4va import sample, feature_probabilities, product_distribution, bdd

class TestBdd4va(unittest.TestCase):

    def test_bdd(self):
        try:
            bdd("model_examples/DellSPLOT/DellSPLOT.xml")
            bdd("model_examples/LargeAutomotive/LargeAutomotive.xml")
        except ExceptionType:
            self.fail("bdd() raised an Exception.")


    def test_sample(self):
        models = glob.glob("model_examples/*/*.dddmp", recursive=True)
        for model in models:
            print("Testing function sample with " + model)
            model = model.replace("\\", "/")
            config_number = randint(1, 10)
            configurations = sample(model, config_number)
            self.assertEqual(len(configurations), config_number)

    def test_feature_probabilities_and_product_distribution(self):
        models = glob.glob("model_examples/*/*.dddmp", recursive=True)
        for model in models:
            print("Testing functions feature_probabilities and product_distribution with " + model)
            model = model.replace("\\", "/")
            probabilities = feature_probabilities(model)
            distribution = product_distribution(model)
            # Distribution has one element more than probabilities:
            # the number of products with zero features activated
            self.assertEqual(len(probabilities), len(distribution) - 1)


if __name__ == '__main__':
    unittest.main()