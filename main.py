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
from libs.learning_lib import constraintsBatchOptimization

from libs.testing_lib import doSomeTests

from libs.basic_stat import getSomeStats

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
    \t----><mutant_root_directory>/\n\
    \t\t---->mutations.xml\n\
    \t\t---->mutants/\n\
    \t\t\t---->mutant_001.xml\n\
    \t\t\t---->mutant_002.xml\n\
    \t\t\t---->...\n\
    \n\
    List of functionalities\n\
    -----------------------\n\
    \t--help: to print help - stop the program after printing\n\
    \t--debug: to enable the debugging mode (for developers)\n\
    "

def main():

    if "--help" in sys.argv:
        print(help())
        sys.exit()

    if "--debug" in sys.argv:
        debug_mode = True
    else:
        debug_mode = False

    if "--visu" in sys.argv:
        visualization = True
    else:
        visualization = False

    try:
        test_directory = sys.argv[1]
    except Exception as excpt:
        raise NoArgument("Please to give at least the XML document (or repository) as argument...")

    #Verification of the path
    if os.path.exists(test_directory):
        if os.path.isfile(test_directory):
            #Transformation of the unique file -> list
            raise RunError("error : need a directory which follow contraints (see help)...")
    else:
        raise FailToLoad("Please to give an existing path for a test directory...")

    #Verification of the XML validation
    for xml_doc in os.listdir(test_directory):
        path_file = "{0}{1}".format(test_directory, xml_doc)
        if os.path.isfile(path_file) and not xml_doc in not_authorized_files:
            print(isValidXMLDocuments(path_file))

    #Creation of the use graph
    use_graph = UseGraph(0, test_directory, debug_mode)

    #Run
    use_graph.run()

if __name__ == '__main__':
    main()
