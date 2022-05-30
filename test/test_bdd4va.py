import unittest
import glob
import os
from random import randint
import re

# Importing bdd4va from a relative path
import sys
sys.path.append("..")
from bdd4va import BDD

class TestBdd4va(unittest.TestCase):

    def test_bdd(self):
        try:
            my_bdd = BDD("model_examples/pizzas/pizzas.xml")
            my_bdd = BDD("model_examples/Truck/Truck.xml")
            my_bdd = BDD("model_examples/mobilemedia2/mobilemedia2.xml")
            my_bdd = BDD("model_examples/tankwar/tankwar.xml")
            my_bdd = BDD("model_examples/DellSPLOT/DellSPLOT.xml")
        except ExceptionType:
            self.fail("my_bdd() raised an Exception.")

    def test_sample(self):
        models = glob.glob("model_examples/*/*.dddmp", recursive=True)
        for model in models:
            print("Testing function sample with " + model)
            model = model.replace("\\", "/")
            my_bdd = BDD(model, False)
            config_number = randint(1, 10)
            configurations = my_bdd.sample(config_number)
            self.assertEqual(len(configurations), config_number)

    def test_feature_probabilities_and_product_distribution(self):
        models = glob.glob("model_examples/*/*.dddmp", recursive=True)
        for model in models:
            print("Testing functions feature_probabilities and product_distribution with " + model)
            model = model.replace("\\", "/")
            my_bdd = BDD(model, False)
            probabilities = my_bdd.feature_probabilities()
            distribution = my_bdd.product_distribution()
            # Distribution has one element more than probabilities:
            # the number of products with zero features activated
            self.assertEqual(len(probabilities), len(distribution) - 1)

    def test_count(self):
        models = glob.glob("model_examples/*/*.dddmp", recursive=True)
        for model in models:
            print("Testing function count with " + model)
            model = model.replace("\\", "/")
            my_bdd = BDD(model, False)
            confs = my_bdd.count()

if __name__ == '__main__':
    unittest.main()