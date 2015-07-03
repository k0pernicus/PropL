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
from libs.utils_lib import cleanCSVFile

from libs.tex_lib import initTexFile
from libs.tex_lib import cleanTexFile
from libs.tex_lib import beginTabular
from libs.tex_lib import closeTabular
from libs.tex_lib import closeTexFile
from libs.tex_lib import writeIntoTexFile

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
    \tprogram <test_directory> [--options]\n\
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
    \t--save_tex: to save results in a tex file\n\
    \t--save_csv: to save results in a CSV file\n\
    \t--clean_tex: to clean the tex file before to write in\n\
    \t--clean_csv: to clean the CSV file before to write in\n\
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

    if "--clean_csv" in sys.argv:
        cleanCSVFile()

    if "--clean_tex" in sys.argv:
        cleanTexFile()

    if "--save_csv" in sys.argv:
        save_results_csv = True
    else:
        save_results_csv = False

    if "--save_tex" in sys.argv:
        save_results_tex = True
    else:
        save_results_tex = False

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

    print("#### Algorithms available")
    print("# dicho_online_opt")
    print("# min_max_online_opt")
    print("# update_all_edges_online_opt")
    print("# tag_on_usefull_edges")
    # print("# constraints_batch_opt")

    algorithm_choosen = input("Which one? ")

    print("")

    list_dir = os.listdir(test_directory)

    usegraph_files = [dir for dir in list_dir if 'usegraph' in dir]

    if save_results_tex:
        initTexFile()
        #7 by default -> some infos about use graph + precision, recall, fscore
        beginTabular(7)

    for usegraph_choosen in usegraph_files:

        print("actual usegraph: {0}".format(usegraph_choosen))

        list_mutation_dir = os.listdir("{0}{1}".format(test_directory, "mutations/"))

        list_mutation_operators = [mut for mut in list_mutation_dir if not mut in not_authorized_files]

        print(list_mutation_operators)

        for mutation_operator in list_mutation_operators:

            Thread(target=computePropagation, args=(nb_of_tests, algorithm_choosen, test_directory, usegraph_choosen, mutation_operator, debug_mode, save_results_csv, save_results_tex)).start()

    if save_results_tex:
        closeTabular()
        closeTexFile()

def computePropagation(nb_of_tests, algorithm_choosen, test_directory, usegraph_choosen, mutation_operator, debug_mode, save_results_csv, save_results_tex):

    print("actual mutation operator: {0}".format(mutation_operator))

    list_precisions = []

    list_recalls = []

    list_fscores = []

    for i in range(0, nb_of_tests):

        #Creation of the use graph
        use_graph = UseGraph("{0}/{1}--{0}".format(usegraph_choosen, mutation_operator, algorithm_choosen), test_directory, usegraph_choosen, mutation_operator, debug_mode)

        #Run
        use_graph.run()

        if "dicho_online_opt" in use_graph.id:
            dichotomicOnlineOptimization(use_graph)

        if "min_max_online_opt" in use_graph.id:
            minAndMaxOnlineOptimization(use_graph)

        if "update_all_edges_online_opt" in use_graph.id:
            updateAllEdgesOnlineOptimization(use_graph)

        if "tag_on_usefull_edges" in use_graph.id:
            tagEachUsefullEdgesOptimization(use_graph)

        # if use_graph.id == "constraints_batch_opt":
        #     constraintsBatchOptimization(use_graph)

        # if visualization:
        #     use_graph.visualize()
        # if infos:
        #     getSomeStats(use_graph)
        precision_tmp, recall_tmp, fscore_tmp = doSomeTests(use_graph)

        list_precisions.append(precision_tmp)
        list_recalls.append(recall_tmp)
        list_fscores.append(fscore_tmp)

        print("Test {0} for {1}... ok!".format(i, use_graph.id))

    list_precisions.sort()
    list_recalls.sort()
    list_fscores.sort()

    len_list_precisions = len(list_precisions)
    len_list_recalls = len(list_recalls)
    len_list_fscores = len(list_fscores)

    median_list_precisions = round(len_list_precisions / 2)
    median_list_recalls = round(len_list_recalls / 2)
    median_list_fscores = round(len_list_fscores / 2)

    if len_list_precisions % 2 != 0:
        precision_to_return = (list_precisions[median_list_precisions] + list_precisions[median_list_precisions + 1]) / 2
    else:
        precision_to_return = list_precisions[median_list_precisions]

    if len_list_recalls % 2 != 0:
        recall_to_return = (list_recalls[median_list_recalls] + list_recalls[median_list_recalls + 1]) / 2
    else:
        recall_to_return = list_recalls[median_list_recalls]

    if len_list_fscores % 2 != 0:
        fscore_to_return = (list_fscores[median_list_fscores] + list_fscores[median_list_fscores + 1]) / 2
    else:
        fscore_to_return = list_fscores[median_list_fscores]

    print("usegraph {0}: P {1} / R {2} / F {3}".format(use_graph.id, precision_to_return, recall_to_return, fscore_to_return))

    dir = test_directory.split("/")[-2]

    if save_results_csv:
        #Write results in a CSV file -> algorithm_choosen, use_graph.id, use_graph.dir, precision, recall, fscore
        writeIntoCSVFile((dir, algorithm_choosen, usegraph_choosen, mutation_operator, round(precision_to_return, 2), round(recall_to_return, 2), round(fscore_to_return, 2)))
    if save_results_tex:
        #Write results in a Tex file
        writeIntoTexFile((dir, algorithm_choosen, usegraph_choosen, mutation_operator, round(precision_to_return, 2), round(recall_to_return, 2), round(fscore_to_return, 2)))

if __name__ == '__main__':
    main()
