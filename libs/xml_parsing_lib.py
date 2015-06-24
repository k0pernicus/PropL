import os

from xml.dom import minidom
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import xml.etree.ElementTree as ET

def parseSmfRun(smf_run_document, debug_mode = False):
    """
    Abstract: Function to parse the smf_run document, which contains all usefull informations about tests.
    Return a dictionary of tests (which contains ids of their methods and variables),\
    a dictionary of test name (to find the id) and a dictionary of case name (to find the id).
    Notice: Each case is a method in the class test!
    """

    tree = ET.parse(smf_run_document)

    root = tree.getroot()

    tests_table = {}

    test_name_to_id = {}

    case_name_to_id = {}

    case_id_to_name = {}

    for test in root.findall("tests"):

        #get classes
        for classes in test.findall("classes"):
            i = 0
            for class_item in classes.findall("class"):

                #build the id
                test_id = "t{0}".format(i)
                test_name = class_item.text

                if debug_mode:
                    print("{0} -> {1}... ".format(test_id, test_name), end="")

                #put the test in the list of available tests
                tests_table[test_id] = { 'name' : test_name, 'items' : [] }

                #save name -> id
                test_name_to_id[test_name] = test_id

                if debug_mode:
                    print("saved!")

                i = i + 1

        if debug_mode:
            print("#"*80)

        nb_of_cases_by_test = {}

        #get cases
        for cases in test.findall("cases"):

            for case_item in cases.findall("case"):

                case_name = case_item.text
                test_id = test_name_to_id[case_name.rsplit('.', 1)[0]]

                if not test_id in nb_of_cases_by_test:
                    nb_of_cases_by_test[test_id] = 0

                i = nb_of_cases_by_test[test_id]

                #search for the test_id to make the case_id & build the id
                case_id = "c{0}".format(i)
                case_id  = test_id + case_id

                if debug_mode:
                    print("{0} ({1}) in {2}... ".format(case_id, case_name, test_id), end="")

                #put the node case in the list of items of the test_id
                tests_table[test_id]['items'].append(case_id)

                #save name -> id
                case_name_to_id[case_name] = {'id' : case_id, 'original_test' : test_id}

                case_id_to_name[case_id] = {'name' : case_name, 'nodes' : []}

                if debug_mode:
                    print("saved!")

                nb_of_cases_by_test[test_id] = i + 1

    return tests_table, test_name_to_id, case_id_to_name, case_name_to_id

def parseMutations(mutations_document, debug_mode = False):
    """
    Abstract: Function to decompose mutations in the xml document (given as parameter), usefull to merge with use graph
    Return a dictionary of mutants id -> name + from + to
    """

    tree = ET.parse(mutations_document)
    root = tree.getroot()

    hash_mutants_table = {}

    mutations_table = {}

    #for each mutant list in the mutations XML file
    for mutants_list in root.findall("mutants"):

        for mutant in mutants_list:

            #if mutant is viable...
            if mutant.get('viable'):
                mutant_name = mutant.get('in')
                if not mutant_name in hash_mutants_table:
                    hash_mutants_table[mutant_name] = {'list_mutants' : []}
                #a mutant id is mxxx, xxx = number of the mutant in the file
                mutant_id = "m{0}".format(mutant.get('id').split('_')[1])
                mutations_table[mutant_id] = {'name': mutant_name, 'from' : mutant.get("from"), 'to' : mutant.get("to"), 'impacted_tests' : []}
                hash_mutants_table[mutant_name]['list_mutants'].append(mutant_id)
                if debug_mode:
                    print("Mutant {0} ({1}) has been added...".format(mutant_name, mutant_id))

    return hash_mutants_table, mutations_table

def joinMutantAndImpactedTests(mutant_file, mutations_table, case_name_to_id, available_mutants, debug_mode = False):
    """
    Abstract: Function to link impacted tests in a single mutant file with cases contains in case_name_to_id
    """

    tree = ET.parse(mutant_file)
    root = tree.getroot()

    mutation_id = "m{0}".format(root.get('id').split('_')[1])

    available_mutants.append(mutation_id)

    if debug_mode:
        print("mutation_id : {0}".format(mutation_id))

    for failing_tests in root.findall("failing"):

        for case_failing_test in failing_tests:

            if debug_mode:
                print("{0} {1}".format(case_failing_test.text,case_name_to_id[case_failing_test.text]))

            mutations_table[mutation_id]['impacted_tests'].append(case_name_to_id[case_failing_test.text])
