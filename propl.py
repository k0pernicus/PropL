#Python3.4 - Antonin Carette

import sys
import os
import datetime

import libs.settings_lib

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

from libs.testing_lib import doSomeTestsWithBrink
from libs.testing_lib import doSomeTestsWithoutBrink

from libs.utils_lib import getSomeInfos
from libs.utils_lib import writeIntoCSVFile
from libs.utils_lib import cleanCSVFile

from libs.tex_lib import initTexFile
from libs.tex_lib import cleanTexFile
from libs.tex_lib import beginTabular
from libs.tex_lib import closeTabular
from libs.tex_lib import closeTexFile
from libs.tex_lib import writeIntoTexFile
from libs.tex_lib import addDefaultTagsIntoTabular

from libs.basic_stat_lib import computeAverage

not_authorized_files = ['.DS_Store', '__init__.py']

algorithms_available = ['dicho_online_opt', 'min_max_online_opt', 'update_all_edges_online_opt', 'tag_on_usefull_edges']

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
    \tprogram <test_directory> <nb_of_tests> [--options]\n\
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
    \t--nb_batch <nbr>: to declare the number of tests to do\n\
    \t--nb_split_tests <nbr>: to declare the proportion of learning tests (1/10 by default)\n\
    \t--usegraph <file>: run the program only for the usegraph <file>\n\
    \t--algorithm <algo>: run the program with the algorithm choosen - the algorithm must be a string which represents the function to execute on data\n\
    \t--all_usegraphs: run the program for all usegraphs (default)\n\
    \t--weight <nbr>: run the program with default weight equals to <nbr> (0.5 by default)\n\
    \t--f_weight <function>: run the program with a custom f_weight (1/log_t, 1/t, 1/square_t, 1/log_square_t)\n\
    \t--rslts_dir <dir>: the directory to save results of tests\n\
    \t--save_tex: to save results in a tex file\n\
    \t--save_csv: to save results in a CSV file\n\
    \t--clean_tex: to clean the tex file before to write in\n\
    \t--clean_csv: to clean the CSV file before to write in\n\
    \t--save_log: to save errors parsing, joining, etc... in a errors.log file\n\
    \t--clean_log: to clean errors.log file\n\
    \t--brink: to compute prediction with brink\n\
    \t--fscore05: to compute fscore with prediction ++\n\
    "

def main():

    if "--help" in sys.argv:
        print(help())
        sys.exit()

    #active the debugging mod
    if "--debug" in sys.argv:
        debug_mode = True
    else:
        debug_mode = False

    #active the visualization of impacted nodes
    if "--visu" in sys.argv:
        visualization = True
    else:
        visualization = False

    #active a mod to have many informations about usefull edges (for impacted nodes), stats, etc...
    if "--infos" in sys.argv:
        infos = True
    else:
        infos = False

    #active a mod to verify and confirm the XML structure of each usefull file
    if "--tests_xml" in sys.argv:
        tests_xml_files = True
    else:
        tests_xml_files = False

    #option to specify the number of batchs to run
    if "--nb_batch" in sys.argv:
        #get the next argument of '--batch'
        nb_batch = int(sys.argv[sys.argv.index("--nb_batch") + 1])
    else:
        nb_batch = 1

    #option to specify the number of slices to do (take one of them to make some tests)
    if "--nb_split_tests" in sys.argv:
        nb_split_tests = int(sys.argv[sys.argv.index("--nb_split_tests") + 1])
    else:
        nb_split_tests = 10

    if "--weight" in sys.argv:
        default_weight = float(sys.argv[sys.argv.index("--weight") + 1])
    else:
        default_weight = 0

    if "--f_weight" in sys.argv:
        f_weight_algo = sys.argv[sys.argv.index("--f_weight") + 1]
    else:
        #default algorithm to compute weights
        f_weight_algo = "default"

    if "--rslts_dir" in sys.argv:
        rslts_dir = sys.argv[sys.argv.index("--rslts_dir") + 1]
    else:
        rslts_dir = "Rslts_propl/"

    #option to clean the csv file before to save results in
    if "--clean_csv" in sys.argv:
        cleanCSVFile()

    #option to clean the tex file before to save results in
    if "--clean_tex" in sys.argv:
        clean_tex = True
    else:
        clean_tex = False

    if "--clean_log" in sys.argv:
        f = open("errors.log", "w")
        f.truncate()
        f.close()

    #option to save results in csv file
    if "--save_csv" in sys.argv:
        save_results_csv = True
    else:
        save_results_csv = False

    #option to save results in tex file
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

    if not '--algorithm' in sys.argv:
        print("#### Algorithms available")
        for algo in algorithms_available:
            print("# {0}".format(algo))

        algorithm_choosen = input("Which one? ")
        print("")
    else:
        algorithm_choosen = sys.argv[sys.argv.index("--algorithm") + 1]
        print("Algorithm \"{0}\" choosen... ".format(algorithm_choosen), end="")
        if algorithm_choosen in algorithms_available:
            print("ok!")
        else:
            print("failure!")
            print("Please to execute the program with one of this available algorithm:")
            for algo in algorithms_available:
                print("\t{0}".format(algo))
            sys.exit()

    if not algorithm_choosen in algorithms_available:
        print("ERROR : Not a correct algorithm...")
        sys.exit()

    list_dir = os.listdir(test_directory)

    if (not '--usegraph' in sys.argv) or ('--all_usegraphs' in sys.argv) :
        usegraph_files = [dir for dir in list_dir if 'usegraph' in dir]
    else:
        usegraph_files =  [sys.argv[sys.argv.index("--usegraph") + 1]]

    for usegraph_choosen in usegraph_files:

        usegraph_base = "{0}_{1}".format(usegraph_choosen.split('.graphml')[0], algorithm_choosen)

        #Condition to clean the tex file
        if clean_tex:
            cleanTexFile("median", rslts_dir, usegraph_base)
            cleanTexFile("average", rslts_dir, usegraph_base)

            #if the user wants to save the results, so we initialize the tex file with a new array
            if save_results_tex:
                 initTexFile("median", rslts_dir, usegraph_base)
                 initTexFile("average", rslts_dir, usegraph_base)
                 #7 by default -> some infos about use graph + precision, recall, fscore
                 beginTabular("median", rslts_dir, usegraph_base, 8)
                 beginTabular("average", rslts_dir, usegraph_base, 8)
                 #add default tags
                 addDefaultTagsIntoTabular("median", rslts_dir, usegraph_base)
                 addDefaultTagsIntoTabular("average", rslts_dir, usegraph_base)

        if debug_mode:
            print("actual usegraph: {0}".format(usegraph_choosen))

        list_mutation_dir = os.listdir("{0}{1}".format(test_directory, "mutations/"))

        list_mutation_operators = [mut for mut in list_mutation_dir if not mut in not_authorized_files]

        if "--mutator" in sys.argv:
            index = sys.argv.index("--mutator") + 1
            while not "--" in sys.argv[index]:
                arg = sys.argv[index]
                for mutation_operator in list_mutation_operators:
                    if arg in mutation_operator:
                        Thread(target=computePropagation, args=(nb_of_tests, usegraph_base, algorithm_choosen, test_directory, rslts_dir, usegraph_choosen, mutation_operator, debug_mode, visualization, infos, nb_batch, default_weight, f_weight_algo, nb_split_tests, save_results_csv, save_results_tex)).start()
                index += 1
        else:
            for mutation_operator in list_mutation_operators:
                Thread(target=computePropagation, args=(nb_of_tests, usegraph_base, algorithm_choosen, test_directory, rslts_dir, usegraph_choosen, mutation_operator, debug_mode, visualization, infos, nb_batch, default_weight, f_weight_algo, nb_split_tests, save_results_csv, save_results_tex)).start()

def computePropagation(nb_of_tests, usegraph_base, algorithm_choosen, test_directory, rslts_dir, usegraph_choosen, mutation_operator, debug_mode, visualization, infos, nb_batch, default_weight, f_weight_algo, nb_split_tests, save_results_csv, save_results_tex):

    if debug_mode:
        print("actual mutation operator: {0}".format(mutation_operator))

    #List which contains precisions computed for the project
    list_precisions = []
    #List which contains recalls computed for the project
    list_recalls = []
    #List which contains f-scores computed for the project
    list_fscores = []
    #List which contains time to compute mutants
    list_times = []

    list_average_precisions = []
    list_average_recalls = []
    list_average_fscores = []

    #initialize the global table for paths
    #This global table will be shared by all usegraph, and reduce the time to compute each path
    libs.settings_lib.init()

    print("Test directory for {1} : {0}".format(test_directory, mutation_operator))

    for i in range(0, nb_of_tests):

        #Creation of the use graph
        use_graph = UseGraph("{0}/{1}--{2}".format(usegraph_choosen, mutation_operator, algorithm_choosen), test_directory, usegraph_choosen, mutation_operator, default_weight, nb_batch, debug_mode, nb_split_tests)

        #Run
        use_graph.run()

        time_begin = datetime.datetime.now()

        if "dicho_online_opt" in use_graph.id:
            dichotomicOnlineOptimization(use_graph)
        elif "min_max_online_opt" in use_graph.id:
            minAndMaxOnlineOptimization(use_graph, f_weight_algo)
        elif "update_all_edges_online_opt" in use_graph.id:
            updateAllEdgesOnlineOptimization(use_graph, f_weight_algo)
        elif "tag_on_usefull_edges" in use_graph.id:
            tagEachUsefullEdgesOptimization(use_graph)

        time_end = datetime.datetime.now()

        time_tmp = time_end - time_begin

        if visualization:
            use_graph.visualize()
        if infos:
            getSomeInfos(use_graph)

        if "--brink" in sys.argv:
            precision_tmp, recall_tmp, fscore_tmp, ave_precision, ave_recall, ave_fscore = doSomeTestsWithBrink(use_graph, algorithm_choosen)
        else:
            precision_tmp, recall_tmp, fscore_tmp, ave_precision, ave_recall, ave_fscore = doSomeTestsWithoutBrink(use_graph, algorithm_choosen)

        list_precisions.append(precision_tmp)
        list_recalls.append(recall_tmp)
        list_fscores.append(fscore_tmp)
        list_times.append(time_tmp)

        list_average_precisions.append(ave_precision)
        list_average_recalls.append(ave_recall)
        list_average_fscores.append(ave_fscore)

        print("Test {0} for {1}... ok ({2})!".format(i, use_graph.id, time_tmp))

    list_precisions.sort()
    list_recalls.sort()
    list_fscores.sort()
    list_times.sort()

    len_list_precisions = len(list_precisions)
    len_list_recalls = len(list_recalls)
    len_list_fscores = len(list_fscores)
    len_list_times = len(list_times)

    median_list_precisions = round(len_list_precisions / 2)
    median_list_recalls = round(len_list_recalls / 2)
    median_list_fscores = round(len_list_fscores / 2)
    median_list_times = round(len_list_times / 2)

    if len_list_precisions % 2 == 0:
        precision_to_return = (list_precisions[median_list_precisions] + list_precisions[median_list_precisions - 1]) / 2
    else:
        precision_to_return = list_precisions[median_list_precisions]

    if len_list_recalls % 2 == 0:
        recall_to_return = (list_recalls[median_list_recalls] + list_recalls[median_list_recalls - 1]) / 2
    else:
        recall_to_return = list_recalls[median_list_recalls]

    if len_list_fscores % 2 == 0:
        fscore_to_return = (list_fscores[median_list_fscores] + list_fscores[median_list_fscores - 1]) / 2
    else:
        fscore_to_return = list_fscores[median_list_fscores]

    if len_list_times % 2 == 0:
        time_to_return = (list_times[median_list_times] + list_times[median_list_times - 1]) / 2
    else:
        time_to_return = list_times[median_list_times]

    #AVERAGE SCORES
    average_precision_to_return = computeAverage(list_average_precisions)
    average_recall_to_return = computeAverage(list_average_recalls)
    average_fscore_to_return = computeAverage(list_average_fscores)

    print("usegraph {0}: P {1} / R {2} / F {3} / T {4}".format(use_graph.id, precision_to_return, recall_to_return, fscore_to_return, time_to_return))

    dir = test_directory.split("/")[-2]

    if save_results_csv:
        #Write results in a CSV file -> algorithm_choosen, use_graph.id, use_graph.dir, precision, recall, fscore
        writeIntoCSVFile(("median", dir, rslts_dir, algorithm_choosen, usegraph_choosen, use_graph.nb_batch, mutation_operator, round(precision_to_return, 2), round(recall_to_return, 2), round(fscore_to_return, 2)))
    if save_results_tex:
        #Write results in a Tex file
        writeIntoTexFile("median", rslts_dir, usegraph_base, (dir, algorithm_choosen, usegraph_choosen, use_graph.nb_batch, mutation_operator, round(precision_to_return, 2), round(recall_to_return, 2), round(fscore_to_return, 2)))

    if save_results_csv:
        #Write results in a CSV file -> algorithm_choosen, use_graph.id, use_graph.dir, precision, recall, fscore
        writeIntoCSVFile(("average", dir, rslts_dir, algorithm_choosen, usegraph_choosen, use_graph.nb_batch, mutation_operator, round(average_precision_to_return, 2), round(average_recall_to_return, 2), round(average_fscore_to_return, 2)))
    if save_results_tex:
        #Write results in a Tex file
        writeIntoTexFile("average", rslts_dir, usegraph_base, (dir, algorithm_choosen, usegraph_choosen, use_graph.nb_batch, mutation_operator, round(average_precision_to_return, 2), round(average_recall_to_return, 2), round(average_fscore_to_return, 2)))


if __name__ == '__main__':
    main()
