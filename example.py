from bdd4va.bdd4va import BDD
import pprint
pp = pprint.PrettyPrinter(indent=4)

# Synthesize a BDD for model DellSPLOT
my_bdd = BDD("/mount/test/model_examples/DellSPLOT/DellSPLOT.xml")

# Generate a sample with 10 configurations
configurations = my_bdd.sample(10)
pp.pprint(configurations)