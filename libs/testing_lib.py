#Python3.4 - Antonin Carette

import sys
import random
from libs.xml_parsing_lib import returnSomeInfosAboutTestFiles
from libs.basic_stat_lib import computePrecision
from libs.basic_stat_lib import computeRecall
from libs.basic_stat_lib import computeFScore
from libs.basic_stat_lib import computeAverage

def isAlgorithmGoodBetween(path, test_dir, files_for_tests, cases_name, mutants_table, nodes_name, tree_learned, debug_mode):
    """
    Function to match the learning results with the principal results of the usegraph.
    This function returns the precision, the recall and the f-score of the match.
    path: The path of the project
    test_dir: The name directory of the tests
    files_for_tests: The files for tests
    cases_name: All cases name
    mutants_table: A table which contains mutants of the usegraph
    nodes_name: All nodes name
    tree_learned: The tree (a small usegraph) learned by some learning algorithms (in libs/learning_lib)
    debug_mode: Debug mode
    """

    #name directory of root mutants files
    root_directory_name = "mutations/{0}".format(test_dir)

    #name directory of mutants files
    mutants_directory_name = "mutants"

    base_path = "{0}{1}/{2}/".format(path, root_directory_name, mutants_directory_name)

    tree_test = returnSomeInfosAboutTestFiles(base_path, files_for_tests, cases_name, mutants_table, nodes_name, debug_mode)

    if debug_mode:
        print("TREE_TEST {0}".format(tree_test))
        print("TREE LEARNED {0}".format(tree_learned))

    precision_to_return = 0

    recall_to_return = 0

    fscore_to_return = 0

    list_precisions = []

    list_recalls = []

    list_fscores = []

    #for each node in tree_test, see all impacted test and add it in tree_test_impacted_tests
    for node in tree_test:

        for mutation_position in tree_test[node]:
            
            list_for_tree_learned = tree_learned[node][mutation_position]

            list_for_tree_tested = tree_test[node][mutation_position]

            if (len(tree_learned[node]) != len(tree_test[node])):
                print("ERROR : lengths between tree learned and tree tested are differents! {0} for learning / {1} for testing".format(len(tree_learned[node]), len(tree_test[node])))
                sys.exit()

            len_items_available_learning = len(list_for_tree_learned)

            len_items_available_testing = len(list_for_tree_tested)

            for i in range(0, len_items_available_learning):
                list_for_tree_learned[i] = list_for_tree_learned[i].split('-')[0]

            for i in range(0, len_items_available_testing):
                list_for_tree_tested[i] = list_for_tree_tested[i].split('-')[0]

            if "--dev_testing" in sys.argv:
                print("LIST TESTED: {0}".format(list_for_tree_tested))
                print("(BEFORE) LIST LEARNED: {0} ----- ".format(list_for_tree_learned), end="")

            true_positive = 0

            false_positive = 0

            false_negative = 0

            for impacted_test in list_for_tree_tested:
                if impacted_test in list_for_tree_learned:
                    true_positive += 1
                    list_for_tree_learned.remove(impacted_test)
                else:
                    false_negative += 1

            #Compute false positive as results still in the list
            false_positive = len(list_for_tree_learned)

            precision = computePrecision(true_positive, false_positive)
            recall = computeRecall(true_positive, false_negative)
            fscore = computeFScore(precision, recall)

            if "--dev_testing" in sys.argv:
                print("(AFTER) LIST LEARNED: {0}".format(list_for_tree_learned))
                print("TP {0} / FP {1} / FN {2}".format(true_positive, false_positive, false_negative))
                print("P {0} / R {1} / F {2}".format(precision, recall, fscore))

            list_precisions.append(precision)
            list_recalls.append(recall)
            list_fscores.append(fscore)

    list_precisions.sort()
    list_recalls.sort()
    list_fscores.sort()

    len_list_precisions = len(list_precisions)
    len_list_recalls = len(list_recalls)
    len_list_fscores = len(list_fscores)

    print("LEN P: {0}".format(len_list_precisions))
    print("LEN R: {0}".format(len_list_recalls))
    print("LEN F: {0}".format(len_list_fscores))

    median_list_precisions = round(len_list_precisions / 2)
    median_list_recalls = round(len_list_recalls / 2)
    median_list_fscores = round(len_list_fscores / 2)

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

    average_precision = computeAverage(list_precisions)
    average_recall = computeAverage(list_recalls)
    average_fscore = computeAverage(list_fscores)

    #return them
    return precision_to_return, recall_to_return, fscore_to_return, average_precision, average_recall, average_fscore

def doSomeTests(usegraph):
    """
    Function to build a learning tree, and return the precision, the recall and the f-score
    usegraph: The usegraph to build the learning tree
    """

    #the learning tree is a simple dictionary, which each key is a node, and the value is a list of impacted tests
    tree = {}

    for (node, mutation_position) in usegraph.nodes_for_tests:

        if usegraph.debug_mode:
            print("node {0}".format(node))

        #put an empty list if the node is not a key in the learning tree
        if not node in tree:
            tree[node] = {}

        tree[node][mutation_position] = []

        #nodes_stack is a stack of visited nodes
        nodes_stack = []

        #all visited nodes for a source node
        visited_nodes = []

        nodes_stack.append(node)

        visited_nodes.append(node)

        #if the stack is empty, we finish...
        while len(nodes_stack) != 0:

            active_node_id = nodes_stack.pop()

            #get the node name by the id
            active_node_name = usegraph.all_nodes_id[active_node_id]

            if usegraph.debug_mode:
               print("active_node_name {0} / successors {1}".format(active_node_name, usegraph.all_nodes_name[active_node_name]['sources']))

            for source_node_id in usegraph.all_nodes_name[active_node_name]['sources']:

                #get the source node name of the node name id
                source_node_name = usegraph.all_nodes_id[source_node_id]

                if usegraph.debug_mode:
                   print("\tsource_node_name {0}".format(source_node_name))

                #the weight of the interesting edge
                weight_edge = usegraph.all_weights[usegraph.all_nodes_position_in_weights_matrix[source_node_id]][usegraph.all_nodes_position_in_weights_matrix[active_node_id]]

                #print("weight between {0} and {1} : {2}".format(source_node_id, active_node_id, weight_edge))

                #get the random_propagation...
                random_propagation = random.uniform(0,1)

                if usegraph.debug_mode:
                   print("random_propagation {0}".format(random_propagation))

                #if the random number is <= weight_edge, the propagation of the bug is acceptable!
                if random_propagation <= weight_edge :

                    if usegraph.debug_mode:
                       print("\trandom_propagation <= weight of source_node_name ({0})".format(weight_edge))

                    #if not 'nt' -> it's a test node!!!!!! WE DID IT! \o/
                    if not 'nt' in source_node_id:

                        #add it in the list of impacted tests if he's not in the list already
                        if not source_node_id in tree[node][mutation_position]:
                            tree[node][mutation_position].append(source_node_id)

                        if usegraph.debug_mode:
                           print("\t{0} saved!".format(source_node_name))

                    #else, add the node in the list to study it later
                    else:

                        if not source_node_id in visited_nodes:

                            if usegraph.debug_mode:
                               print("\t{0} append...".format(source_node_name))

                            nodes_stack.append(source_node_id)
                            visited_nodes.append(source_node_id)

                else:

                    if usegraph.debug_mode:
                       print("\trandom_propagation > weight of source_node_name ({0})".format(weight_edge))

                       visited_nodes.append(source_node_id)

    #compute the precision, the recall and the f-score!
    precision_compt, recall_comp, fscore_comp, ave_precision, ave_recall, ave_fscore = isAlgorithmGoodBetween(usegraph.path_file, usegraph.mutation_operator, usegraph.files_for_tests, usegraph.all_cases_name, usegraph.mutants, usegraph.all_nodes_name, tree, usegraph.debug_mode)

    #return the precision, the recall and the f-score
    return precision_compt, recall_comp, fscore_comp, ave_precision, ave_recall, ave_fscore
