from platform import system
import os
import subprocess, locale
import re
from pathlib import Path

def set_global_constants():
    '''
    Private auxiliary function that configures the following global constants:
        + SYSTEM, which stores the operating system running bdd4va: Linux or Windows.
        + BDD4VAR_DIR, which stores the path of the module bdd4va, which is needed to locate the binaries.
    '''
    global SYSTEM, BDD4VAR_DIR
    # get SYSTEM
    SYSTEM = system()
    # get BDD4VAR_DIR
    caller_dir = os.getcwd()
    os.chdir(Path(__file__).parent)
    if SYSTEM == 'Windows':
        shell = subprocess.run(['wsl', 'pwd'], stdout=subprocess.PIPE)
    else:
        shell = subprocess.run(['pwd'], stdout=subprocess.PIPE)
    BDD4VAR_DIR = shell.stdout.decode(locale.getdefaultlocale()[1]).strip()
    os.chdir(caller_dir)
set_global_constants()

def run(binary, *args):
    '''
    Private auxiliary function to run binary files in Linux and Windows.    
    '''
    bin_file = BDD4VAR_DIR + "/bin/" + binary
    if SYSTEM == 'Windows':
        if not args:
            command = ['wsl', bin_file]
        else:
            command = ['wsl', bin_file] + list(args)
    else:
        if not args:
            command = [bin_file]
        else:
            command = [bin_file] + list(args)
    return subprocess.run(command, stdout=subprocess.PIPE)

def check_file_existence(filename, extension):
    '''
    Private auxiliary function that verifies if the input file exists    
    '''
    if not os.path.isfile(filename):
        filename = filename + '.' + extension
        if not os.path.isfile(filename):
            message = 'The file "' + filename + '" doesn\'t exist.'
            raise(Exception(message))
    return filename

def bdd(model_file):
    '''
    Builds a BDD for a configuration model
    :param model_file: A file specifying a configuration model with the SPLOT format (visit http://www.splot-research.org/)
    :return: A dddmp file containing the BDD encoding of the model (dddmp is the format that the BDD library CUDD uses;
    check https://github.com/vscosta/cudd). The dddmp file is generated in the same folder where model_file is located.
    '''
    # Check model_file
    model_file = check_file_existence(model_file, "xml")
    file_name = re.search('(.*)[.]xml', model_file).group(1)

    # Run binary splot2logic
    print("Preprocessing " + model_file + " to get its BDD...")
    splot_process = run("splot2logic", "-use-XOR", model_file)
    # Check that splot2logic was successful
    try:
        check_file_existence(file_name, "var")
        check_file_existence(file_name, "exp")
    except Exception:
        message = 'BDD synthesis failed: the files "' + file_name + '.var" and "' + \
                  file_name + '.exp" couldn\'t be generated.'
        raise (Exception(message))

    # Run binary logic2bdd's execution
    print("Synthesizing the BDD (this may take a while)...")
    bdd_process = run("logic2bdd",
                      "-line-length", "50",
                      "-min-nodes", "100000",
                      "-constraint-reorder", "minspan",
                      "-base", file_name,
                      file_name + ".var",
                      file_name + ".exp")
    # Check that logic2bdd's execution was successful
    try:
        check_file_existence(file_name, "dddmp")
    except Exception:
        message = 'BDD synthesis failed: the file "' + file_name + '.dddmp couldn\'t be generated.'
        raise (Exception(message))

    # Remove auxiliary generated files
    AUXILIARY_FILES = [".data", ".exp", ".reorder", ".tree", ".var"]
    for f in AUXILIARY_FILES: Path(file_name + f).unlink()

def sample(bdd_file, config_number, with_replacement=True):
    '''
    Generates a uniform random sample of size "config_number" from "bdd_file".
    For detailed information, see the paper: R. Heradio, D. Fernandez-Amoros, J. Galindo,
    D. Benavides, and D. Batory, "Uniform and Scalable Sampling of Highly Configurable Systems,” Submitted
    to Empirical Software Engineering (currently under review), 2021.
    :param bdd_file: dddmp file that stores a configuration model's BDD encoding (dddmp is the
           format that the BDD library CUDD uses; check https://github.com/vscosta/cudd)
    :param config_number: Number of configurations to be generated.
    :param with_replacement: If it is True, every configuration is generated from scratch, independently
           of the prior generated configurations. Accordingly, a configuration may be repeated in the sample. If
           with_replacement is False then the sample is generated without replacement and there won't be any
           repeated configurations (for a more detailed explanation, check https://en.wikipedia.org/wiki/Simple_random_sample).
    :return: A list with the generated configurations. Each element in that list is a configuration, and
             each configuration is in turn a list of strings encoding the feature values.
    '''
    # Check bdd_file
    bdd_file = check_file_existence(bdd_file, "dddmp")

    # Check config_number
    if config_number <= 0:
        message = 'config_number must be an integer greater than zero'
        raise(Exception(message))

    # Run binary BDDSampler
    parameters = ["-names"]
    if not with_replacement:
        parameters.append("-norep")
    print("Getting a sample with", config_number, "configurations (this may take a while)...")
    sample_process = run("BDDSampler", "-names", str(config_number), bdd_file)
    result = sample_process.stdout.decode(locale.getdefaultlocale()[1])
    line_iterator = iter(result.splitlines())
    configurations = []
    for line in line_iterator:
        parsed_line = re.compile("\s+").split(line)
        configuration = []
        negation = ""
        for element in parsed_line:
            if element != "":
                if element == "not":
                    negation = "not "
                else:
                    configuration.append(negation + element)
                    negation = ""
        configurations.append(configuration)
    return configurations

def feature_probabilities(bdd_file):
    '''
    Computes the probability each model feature has to be included in a valid product.
    That is, for every feature it returns the number of valid products with the feature activated
    divided by the total number of valid products (a product is valid if it satisfies all model constraints).
    For detailed information, see the paper: Heradio, R., Fernandez-Amoros, D., Mayr-Dorn, C., Egyed, A.:
    Supporting the statistical analysis of variability models. In: 41st International Conference on Software
    Engineering (ICSE), pp. 843–853. Montreal, Canada (2019).
    :param bdd_file: dddmp file that stores a configuration model's BDD encoding (dddmp is the
           format that the BDD library CUDD uses; check https://github.com/vscosta/cudd).
    :return: A dictionary with the format {feature_1: feature_1_probability, feature_2: feature_2_probability, ...}
    '''
    # Check bdd_file
    bdd_file = check_file_existence(bdd_file, "dddmp")

    # Run binary feature_probabilities
    print("Getting the feature probabilities (this may take a while)...")
    bdd_file = re.search('(.*)[.]dddmp', bdd_file).group(1)
    feature_probabilities_process = run("feature_probabilities", bdd_file)
    result = feature_probabilities_process.stdout.decode(locale.getdefaultlocale()[1])
    line_iterator = iter(result.splitlines())
    probabilities = {}
    for line in line_iterator:
        parsed_line = re.compile("\s+").split(line.strip())
        probabilities[parsed_line[0]] = float(parsed_line[1])
    return probabilities

def product_distribution(bdd_file):
    '''
    Computes the distribution of the number of activated features per product.
    That is,
        + How many products have 0 features activated?
        + How many products have 1 feature activated?
        + ...
        + How many products have all features activated?
    For detailed information, see the paper: Heradio, R., Fernandez-Amoros, D., Mayr-Dorn, C., Egyed, A.:
    Supporting the statistical analysis of variability models. In: 41st International Conference on Software
    Engineering (ICSE), pp. 843–853. Montreal, Canada (2019).
    :param bdd_file: dddmp file that stores a configuration model's BDD encoding (dddmp is the
           format that the BDD library CUDD uses; check https://github.com/vscosta/cudd).
    :return: A list that stores:
        + In index 0, the number of products with 0 features activated.
        + In index 1, the number of products with 1 feature activated.
        ...
        + In index n, the number of products with n features activated.
    '''
    # Check bdd_file
    bdd_file = check_file_existence(bdd_file, "dddmp")

    # Run binary product_distribution
    print("Getting the product distribution (this may take a while)...")
    bdd_file = re.search('(.*)[.]dddmp', bdd_file).group(1)
    product_distribution_process = run("product_distribution", bdd_file)
    result = product_distribution_process.stdout.decode(locale.getdefaultlocale()[1])
    line_iterator = iter(result.splitlines())
    distribution = []
    for line in line_iterator:
        parsed_line = re.compile("\s+").split(line.strip())
        distribution.append(int(parsed_line[1]))
    return distribution










