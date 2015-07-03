import sys
import os

from threading import Thread

#from libs.xml_lib import load_xml_document
from libs.xml_lib import isValidXMLDocuments
from libs.xml_lib import isAValidXMLDocument

from libs.exceptions.NoArgument import NoArgument
from libs.exceptions.RunError import RunError

from libs.use_graph_lib import UseGraph

from libs.learning_lib import dichotomicOnlineOptimization
from libs.learning_lib import minAndMaxOnlineOptimization
from libs.learning_lib import updateAllEdgesOnlineOptimization
from libs.learning_lib import tagEachUsefullEdgesOptimization

from libs.testing_lib import doSomeTests

from libs.utils_lib import getSomeInfos
from libs.utils_lib import writeIntoCSVFile
from libs.utils_lib import clearCSVFile

not_authorized_files = ['.DS_Store', '__init__.py']

def help():
    """
    Abstract: Print usage and functionalities of the program
    """

    return "\
    PropL program\n\
    ---------\n\
    ---------\n\
    \n\
    Usage\n\
    -----\n\
    \tprogram <test_directory> [--help|--debug]\n\
    \n\
    Test directory\n\
    --------------\n\
    \t<root>/\n\
    \t---->smf.run.xml\n\
    \t---->usegraph.graphml\n\
    \t---->mutations/\n\
    \t\t----><operator_mutant_directory_1>/\n\
    \t\t\t---->mutations.xml\n\
    \t\t\t---->mutants/\n\
    \t\t\t\t---->mutant_001.xml\n\
    \t\t\t\t---->mutant_002.xml\n\
    \t\t\t\t---->...\n\
    \t\t----><operator_mutant_directory_2>/\n\
    \t\t\t---->mutations.xml\n\
    \t\t\t---->mutants/\n\
    \t\t\t\t---->mutant_001.xml\n\
    \t\t\t\t---->mutant_002.xml\n\
    \t\t\t\t---->...\n\
    \t\t---->...\n\
    \n\
    List of functionalities\n\
    -----------------------\n\
    \t--help: to print help - stop the program after printing\n\
    \t--debug: to enable the debugging mode (for developers)\n\
    \t--visu: to enable the usegraph visualization\n\
    \t--infos: to get some infos about edges, etc...\n\
    \t--tests_xml: to test XML files (available, synthax validation, etc...)\n\
    "

def main():

    if "--help" in sys.argv:
        print(help())
        sys.exit()

    if "--tests_xml" in sys.argv:
        tests_xml_files = True
    else:
        tests_xml_files = False

    if "--debug" in sys.argv:
        debug_mode = True
    else:
        debug_mode = False

    if "--visu" in sys.argv:
        visualization = True
    else:
        visualization = False

    if "--infos" in sys.argv:
        infos = True
    else:
        infos = False

    if "--clear-csv" in sys.argv:
        clearCSVFile()

    if "--save" in sys.argv:
        save_results = True
    else:
        save_results = False

    try:
        test_directory = sys.argv[1]
        nb_of_tests = int(sys.argv[2])
    except Exception as excpt:
        raise NoArgument("Please to give at least the XML document (or repository) as argument...")

    #Verification of the path
    if os.path.exists(test_directory):
        if os.path.isfile(test_directory):
            #Transformation of the unique file -> list
            raise RunError("error : need a directory which follow contraints (see help)...")
    else:
        raise FailToLoad("Please to give an existing path for a test directory...")

    if tests_xml_files:
        #Verification of the XML validation
        for xml_doc in os.listdir(test_directory):
            path_file = "{0}{1}".format(test_directory, xml_doc)
            if os.path.isfile(path_file) and not xml_doc in not_authorized_files:
                print(isValidXMLDocuments(path_file))

    #Creation of the use graph
    use_graph = UseGraph(0, test_directory, debug_mode)

    print("#### Algorithms available")
    print("# baseline")
    print("# dicho_online_opt")
    print("# min_max_online_opt")
    print("# update_all_edges_online_opt")
    print("# tag_on_usefull_edges")
    # print("# constraints_batch_opt")

    algorithm_choosen = input("Which one? ")

    print("")

    use_graph.id = algorithm_choosen

    #Run
    use_graph.run()

    if use_graph.id == "dicho_online_opt":
        dichotomicOnlineOptimization(use_graph)

    if use_graph.id == "min_max_online_opt":
        minAndMaxOnlineOptimization(use_graph)

    if use_graph.id == "update_all_edges_online_opt":
        updateAllEdgesOnlineOptimization(use_graph)

    if use_graph.id == "baseline":
        computeBaseline(use_graph)

    # if use_graph.id == "constraints_batch_opt":
    #     constraintsBatchOptimization(use_graph)

    if visualization:
        use_graph.visualize()
    if infos:
        getSomeStats(use_graph)
    doSomeTests(use_graph)

if __name__ == '__main__':
    main()
