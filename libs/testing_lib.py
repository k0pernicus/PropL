#Python3.4 - Antonin Carette

import random
from libs.xml_parsing_lib import returnSomeInfosAboutTestFiles
from libs.basic_stat_lib import computePrecision
from libs.basic_stat_lib import computeRecall
from libs.basic_stat_lib import computeFScore

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

    #true_positive is a positive test found, which is positive too
    true_positive = 0

    #false_positive is a positive test found, which is not positive
    false_positive = 0

    #false_negative is a negative test found, which is positive
    false_negative = 0

    #impacted tests for tree test
    tree_test_impacted_tests = []

    #impacted tests for tree learned
    tree_learned_impacted_tests = []

    #for each node in tree_test, see all impacted test and add it in tree_test_impacted_tests
    for node in tree_test:
        for impacted_test in tree_test[node]:
            tree_test_impacted_tests.append(impacted_test.split('-')[0])

    #for each node in tree_learned, see all impacted test and add it in tree_learned_impacted_tests
    for node in tree_learned:
        for impacted_test in tree_learned[node]:
            tree_learned_impacted_tests.append(impacted_test.split('-')[0])

    #remove duplications
    tree_test_impacted_tests = list(set(tree_test_impacted_tests))
    tree_learned_impacted_tests = list(set(tree_learned_impacted_tests))

    #compute precision, recall and fscore
    for node in tree_learned_impacted_tests:
        if node in tree_test_impacted_tests:
            true_positive += 1

    false_positive = len(tree_learned_impacted_tests) - true_positive
    false_negative = len(tree_test_impacted_tests) - true_positive

    precision = computePrecision(true_positive, false_positive)
    recall = computeRecall(true_positive, false_negative)
    fscore = computeFScore(precision, recall)

    #return them
    return precision, recall, fscore

def doSomeTests(usegraph):
    """
    Function to build a learning tree, and return the precision, the recall and the f-score
    usegraph: The usegraph to build the learning tree
    """

    #the learning tree is a simple dictionary, which each key is a node, and the value is a list of impacted tests
    tree = {}

    for node in usegraph.nodes_for_tests:

        if usegraph.debug_mode:
            print("node {0}".format(node))

        #put an empty list if the node is not a key in the learning tree
        if not node in tree:
            tree[node] = []

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
                        if not source_node_id in tree[node]:
                            tree[node].append(source_node_id)

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
    precision_compt, recall_comp, fscore_comp = isAlgorithmGoodBetween(usegraph.path_file, usegraph.mutation_operator, usegraph.files_for_tests, usegraph.all_cases_name, usegraph.mutants, usegraph.all_nodes_name, tree, usegraph.debug_mode)

    #return the precision, the recall and the f-score
    return precision_compt, recall_comp, fscore_comp
