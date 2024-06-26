# bdd4va (BDDs for Variability Analysis)

A Python library for the analysis of highly configurable systems. 

## Contents

  * [Description](#description)
  * [Requirements and Installation](#requirements-and-installation)
  * [Usage Example](#usage-example)
  * [Detailed Function Documentation](#detailed-function-documentation)
  * [Flama](#flama)

## Description

bdd4va supports the analysis of variability models specified with the [SPLOT format](http://www.splot-research.org/). To do so, it first creates a [Binary Decision Diagram (BDD)](https://github.com/vscosta/cudd) that is later explored. In particular, bdd4va supports the following operations:

+ **BDD Synthesis**: bdd4va wraps the [Logic2BDD tool](https://github.com/davidfa71/Extending-Logic) to build BDDs, which was presented in [*D. Fernandez-Amoros, S. Bra, E. Aranda-Escolastico, and R. Heradio, "Using Extended Logical Primitives for Efficient BDD Building," Mathematics, vol. 8, no. 8, p. 1253, 2020.*](https://www.mdpi.com/2227-7390/8/8/1253)
+ **Counting the total number of valid configurations** 
+ **Uniform Random Sampling**: bdd4va generates configuration samples *with* and *without replacement*. To do so, it wraps [BDDSampler](https://github.com/davidfa71/BDDSampler), which was presented in [*R. Heradio, D. Fernandez-Amoros, J. Galindo, D. Benavides, and D. Batory, "Uniform and Scalable Sampling of Highly Configurable Systems", Empirical Software Engineering, vol. 27, no. 44, 2022.*](https://doi.org/10.1007/s10664-021-10102-5)
+ **Computing Feature Probabilities**: bdd4va gets the probability each model feature has to be included in a valid product. That is, for every feature it returns the number of valid products with the feature activated divided by the total number of valid products (a product is valid if it satisfies all model constraints). For that, it wraps the tool [probability](https://github.com/rheradio/VMStatAnal), which was described in [*Heradio, R., Fernandez-Amoros, D., Mayr-Dorn, C., Egyed, A.: "Supporting the statistical analysis of variability models". 41st International Conference on Software Engineering (ICSE), pp. 843–853. Montreal, Canada (2019).*](https://ieeexplore.ieee.org/document/8811977).
+ **Computing Product Distribution**:  bdd4va gets the distribution of the number of activated features per product. That is,
        
        + How many products have 0 features activated?
        + How many products have 1 feature activated?
        + ...
        + How many products have all features activated?
    
    To do so, bdd4va wraps the tool [histogram](https://github.com/rheradio/VMStatAnal), which was described in [*Heradio, R., Fernandez-Amoros, D., Mayr-Dorn, C., Egyed, A.: "Supporting the statistical analysis of variability models". In: 41st International Conference on Software Engineering (ICSE), pp. 843–853. Montreal, Canada (2019).*](https://ieeexplore.ieee.org/document/8811977).

## Requirements and Installation

bdd4va has been tested on Linux and Windows with Python 3.8.10. For Windows, it requires installing the [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install).

Imagine bdd4va has been downloaded into the directory <tt>my_folder</tt>. Go to that directory:
```
cd my_folder
```
and run
```
pip install ./bdd4va
```

## Usage Example

The following code:
1) Imports bdd4va.
2) Imports the library pprint for pretty-printing the results.
3) Creates a BDD for the [Dell laptop configurator variability model](https://github.com/rheradio/bdd4va/blob/main/test/model_examples/DellSPLOT/DellSPLOT.xml) included in the [test folder](https://github.com/rheradio/bdd4va/tree/main/test).
4) Counts the total number of valid configurations when there is no feature assignment
5) Counts the total number of valid configurations for a partial feature assignment
6) Generates a sample with 10 configurations and then prints the result.
7) Computes the feature probabilities and then prints the result.
8) Computes the product distribution and then prints the result.
9) Shows how to use a previously synthesized BDD file 

```
from bdd4va.bdd4va import BDD
import pprint
pp = pprint.PrettyPrinter(indent=4)

# Synthesize a BDD for model DellSPLOT
my_bdd = BDD("test/model_examples/DellSPLOT/DellSPLOT.xml")

# Count the total number of valid configurations
confs = my_bdd.count()
print(confs)

# Count the number of valid configurations
# * With features Vostro_1510 and Hardware_Raid not activated
# * With feature Latitude_D630N activated
confs = my_bdd.count(['not Vostro_1510', 'Latitude_D630N', 'not Hardware_Raid'])
print(confs)

# Generate a sample with 10 configurations
configurations = my_bdd.sample(10)
pp.pprint(configurations)

# Compute the feature probabilities
probabilities = my_bdd.feature_probabilities()
pp.pprint(probabilities)

# Compute the product distribution
distribution = my_bdd.product_distribution()
pp.pprint(distribution)

# When a BDD is synthesized, it is automatically stored in a dddmp file.
# Accordingly and to save time, if the BDD hasn't changed, you don't need to synthesize it again!!
# For example, we can create a new BDD object reusing our previously
# synthesized bdd. To do so,
# 1) The model_file param is the dddmp file
# 2) The synthesize_bdd param of BDD is set to False

# Reuse a previously synthesized BDD
my_restored_bdd = BDD("test/model_examples/DellSPLOT/DellSPLOT.dddmp", False)
configurations = my_restored_bdd.sample(10)
pp.pprint(configurations)
```

The code execution would print the following text:

```
Preprocessing test/model_examples/DellSPLOT/DellSPLOT.xml to get its BDD...
Synthesizing the BDD (this may take a while)...

Counting the number of valid configurations (this may take a while)...
1128674

Counting the number of valid configurations (this may take a while)...
5760

Getting a sample with 10 configurations (this may take a while)...
[   [   'Dell_XML',
        'not Vostro_1510',
        ...,
        'not integrated_Modem'
    ],
    ...
]

Getting the feature probabilities (this may take a while)...
{   'Beetwen_5_and_7_lbs_Light': 0.869268,
    'Between_1000_1300': 0.181764,
    ...
    'w80211n': 0.0803492
}

Getting the product distribution (this may take a while)...
[   0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    22108,
    103540,
    223702,
    ...
]
```

For more examples, see the [bdd4va test](https://github.com/rheradio/bdd4va/blob/main/test/test_bdd4va.py).

## Detailed Function Documentation

### __init__(self, model_file, synthesize_bdd=True)
    Builds a BDD for a configuration model
    :param model_file: A file specifying a configuration model with the SPLOT format.
    :param synthesize_bdd: do you like to synthesize the BDD or to restore a previously synthesized one?
    :return: A dddmp file containing the BDD encoding of the model is generated in the same folder where model_file is located.
    
### count(self, feature_assignment=[]):
    Computes the number of valid configurations.
    :param feature_assignment: a list with a partial or a complete features' assignment
           (e.g., ["f1", "not f3", "f5"])
    :return The number of valid configurations
             
### sample(self, config_number, with_replacement=True)
    Generates a uniform random sample of size "config_number" from "bdd_file".
    :param config_number: Number of configurations to be generated.
    :param with_replacement: If it is True, every configuration is generated from scratch, independently
           of the prior generated configurations. Accordingly, a configuration may be repeated in the sample. If
           with_replacement is False then the sample is generated without replacement and there won't be any
           repeated configurations (for a more detailed explanation, check https://en.wikipedia.org/wiki/Simple_random_sample).
    :return: A list with the generated configurations. Each element in that list is a configuration, and
             each configuration is in turn a list of strings encoding the feature values.

### feature_probabilities(self, feature_assignment=[]):
    Computes the probability each model feature has to be included in a valid product.
    That is, for every feature it returns the number of valid products with the feature activated
    divided by the total number of valid products (a product is valid if it satisfies all model constraints).
    For detailed information, see the paper: Heradio, R., Fernandez-Amoros, D., Mayr-Dorn, C., Egyed, A.:
    Supporting the statistical analysis of variability models. In: 41st International Conference on Software
    Engineering (ICSE), pp. 843–853. Montreal, Canada (2019).
    :param feature_assignment: a list with a partial or a complete features' assignment
           (e.g., ["f1", "not f3", "f5"])
    :return: A dictionary with the format {feature_1: feature_1_probability, feature_2: feature_2_probability, ...}

### product_distribution(self):
    Computes the distribution of the number of activated features per product.
    :return: A list that stores:
        + In index 0, the number of products with 0 features activated.
        + In index 1, the number of products with 1 feature activated.
        ...
        + In index n, the number of products with n features activated.

## Flama

bdd4va is intended to be part of [Flama](https://github.com/diverso-lab/core), which is a Python-based framework for the Automated Analysis of Feature Models (AAFM). It takes into consideration previous AAFM tool designs and enables multi-solver and multi-metamodel support for the integration of AAFM tooling on the Python ecosystem.

The main features of the framework are:

+ Easy to extend by enabling the creation of new plugins following a semi-automatic generator approach.
+ Support multiple variability models. Currently, it provides support for cardinality-based feature models. However, it is easy to integrate others such as attributed feature models.
+ Support multiple solvers. Currently, it provides support for the PySAT metasolver, which enables more than ten different solvers.
+ Support multiple operations. It is developed, having in mind multi-model operations such as those depicted by Familiar and single-model operations.

