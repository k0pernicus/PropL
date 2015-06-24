import random
from libs.xml_parsing_lib import returnSomeInfosAboutTestFiles

#name directory of root mutants files
root_directory_name = "AOR"

#name directory of mutants files
mutants_directory_name = "mutants"

def isAlgorithmGoodBetween(path, files_for_tests, cases_name, mutants_table, nodes_name, tree_learned):

    base_path = "{0}{1}/{2}/".format(path, root_directory_name, mutants_directory_name)

    tree_test = returnSomeInfosAboutTestFiles(base_path, files_for_tests, cases_name, mutants_table, nodes_name)

    print("TREE_TEST {0}".format(tree_test))

    print("TREE LEARNED {0}".format(tree_learned))

def doSomeTests(usegraph):

    tree = {}

    for node in usegraph.nodes_for_tests:

        if usegraph.debug_mode:
            print("node {0}".format(node))

        tree[node] = []

        nodes_stack = []

        nodes_stack.append(node)

        while len(nodes_stack) != 0:

            active_node_id = nodes_stack.pop()

            active_node_name = usegraph.all_nodes_id[active_node_id]

            if usegraph.debug_mode:
                print("active_node_name {0} / successors {1}".format(active_node_name, usegraph.all_nodes_name[active_node_name]['sources']))

            for source_node_id in usegraph.all_nodes_name[active_node_name]['sources']:

                source_node_name = usegraph.all_nodes_id[source_node_id]

                if usegraph.debug_mode:
                    print("\tsource_node_name {0}".format(source_node_name))

                weight_node = usegraph.all_weights[usegraph.all_nodes_position_in_weights_matrix[source_node_id]][usegraph.all_nodes_position_in_weights_matrix[active_node_id]]

                random_propagation = random.uniform(0,1)

                if usegraph.debug_mode:
                    print("random_propagation {0}".format(random_propagation))

                if random_propagation <= weight_node :

                    if usegraph.debug_mode:
                        print("\trandom_propagation <= weight of source_node_name ({0})".format(weight_node))

                    if not 'nt' in source_node_id:

                        if not source_node_id in tree[node]:
                            tree[node].append(source_node_id)

                        if usegraph.debug_mode:
                            print("\t{0} saved!".format(source_node_name))

                    else:

                        if usegraph.debug_mode:
                            print("\t{0} append...".format(source_node_name))
                        nodes_stack.append(source_node_id)

                else:

                    if usegraph.debug_mode:
                        print("\trandom_propagation > weight of source_node_name ({0})".format(weight_node))

    isAlgorithmGoodBetween(usegraph.path_file, usegraph.files_for_tests, usegraph.all_cases_name, usegraph.mutants, usegraph.all_nodes_name, tree)
