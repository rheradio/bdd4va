# bdd4va (BDDs for Variability Analysis)

A Python library for the analysis of highly configurable systems. 

## Description

bdd4va supports the analysis of variability models specified with the [SPLOT format](http://www.splot-research.org/). To do so, it first creates a [Binary Decision Diagram (BDD)](https://github.com/vscosta/cudd) that is later explored. In particular, bdd4va supports the following operations:

+ **BDD Synthesis**. bdd4va wraps the [Logic2BDD tool](https://github.com/davidfa71/Extending-Logic) described in: 

+ **Configurations' Uniform Random Sampling**.
+ **Computing the Feature Probabilities**. 
+ **Computing the Product Distribution**

## FaMaPy

bdd4va is intended to be part of [FaMaPy](https://github.com/diverso-lab/core), which is a Python-based framework for the Automated Analysis of Feature Models (AAFM). It takes into consideration previous AAFM tool designs and enables multi-solver and multi-metamodel support for the integration of AAFM tooling on the Python ecosystem.

The main features of the framework are:

+ Easy to extend by enabling the creation of new plugins following a semi-automatic generator approach.
+ Support multiple variability models. Currently, it provides support for cardinality-based feature models. However, it is easy to integrate others such as attributed feature models.
+ Support multiple solvers. Currently, it provides support for the PySAT metasolver, which enables more than ten different solvers.
+ Support multiple operations. It is developed, having in mind multi-model operations such as those depicted by Familiar and single-model operations.

