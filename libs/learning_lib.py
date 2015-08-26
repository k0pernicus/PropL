#Python3.4 - Antonin Carette

import networkx as nx
import math
import time
import random
import sys
import datetime

import libs.settings_lib

###################
#SIMPLE ALGORITHMS#
###################

def f_weight(f_weight_algo, n_batch = 0, nb_mutants = 0):
    """
    Abstract: Function to return a weight based with t
    """
    if f_weight_algo == "default":
        #Default function : 'c' / (nb_batch * nb_mutants) where 'c' = (40 / (540 / nb_mutants))
        c = (40 / (540 / nb_mutants))
        r = (c / (n_batch * nb_mutants))
        return r
    if f_weight_algo == "1/log_t":
        return 1 / math.log(t + 3000)
    if f_weight_algo == "1/t":
        return 1 / t
    if f_weight_algo == "1/square_t":
        return 1 / math.pow(t, 2)
    if f_weight_algo == "1/square_log_t":
        return 1 / math.pow(math.log(t + 3000), 2)

    #Default function : 'c' / (nb_batch * nb_mutants) where 'c' = (40 / (540 / nb_mutants))
    c = (40 / (540 / nb_mutants))
    r = (c / (n_batch * nb_mutants))
    print("DEFAULT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(r)

    return r

def getMinEdgeFrom(paths, usegraph):
    """
    Abstract: Function to return the id of the edge which have the minimal weight
    paths: All paths between two nodes
    usegraph: The usegraph which are extracts all paths
    """

    #min = 1 (1 is the max of the weight)
    min = 1

    #init a field which is the id of the edge to return
    edge_id = ''

    #search in all paths...
    for all_paths in paths:

        #get list of tuples by these paths
        all_paths = getExistingPathsFrom(all_paths)

        #for each path...
        for p in all_paths:

            #get the id of the edge
            edge = usegraph.transform_edge_name_as_edge_id(p)
            #get the edge by the id, to get source and target nodes
            edge_id_tmp = usegraph.all_edges_name[edge]['id']
            source = usegraph.all_edges_id[edge_id_tmp]['source']
            target = usegraph.all_edges_id[edge_id_tmp]['target']
            #get the weight of the edge
            edge_weight = usegraph.all_weights[usegraph.all_nodes_position_in_weights_matrix[source]][usegraph.all_nodes_position_in_weights_matrix[target]]
            #if the weight is < to the min field, the edge studied get the min weight
            if edge_weight <= min:
                min = edge_weight
                edge_id = edge_id_tmp

    #return the id of the min edge
    return edge_id

def getExistingPathsFrom(path):
    """
    Abstract: Function to transform the list of nodes (all_paths) to a list of tuples (source, target)
    Ex: [node1, node2, node3, node4, ...] -> [(node1, node2),(node2, node3), (node3, node4), (node4,...)]
    path: A path in the usegraph
    """

    return [(path[a], path[a + 1]) for a in range(0, len(path) - 1)]

#################################################
#ALGORITHM TO COMPUTE REPRESENTATION FOR MUTANTS#
#################################################

def computeSimpleRepresentationForAMutant(mutant, usegraph):
    """
    Abstract: Method to return a simple representation for one mutant - a representation is {'mutant_from||mutant_to' : [mutation_id0, mutation_id1, ...]}
    mutant: The base mutant to build the simple representation
    usegraph: The usegraph which the mutant come from
    """

    #the simple representation of a mutant is a simple dictionary
    simple_representation_by_mutant = {}

    #searching for all mutant id in the list of mutants
    for single_mutant_id in usegraph.hash_mutants[mutant]['list_mutants']:

        #this field is a tag to know if there's multiple tests for the same mutation
        position_of_the_mutation = "{0}||{1}".format(usegraph.mutants[single_mutant_id]['from'], usegraph.mutants[single_mutant_id]['to'])

        if not position_of_the_mutation in simple_representation_by_mutant:
            simple_representation_by_mutant[position_of_the_mutation] = []

        #append the mutant id in the representation
        simple_representation_by_mutant[position_of_the_mutation].append(single_mutant_id)

    return simple_representation_by_mutant

def getSimpleRepresentationForMutants(usegraph):
    """
    Abstract: Method to return a representation of which mutant is the child of a father mutant
    usegraph: The usegraph object which mutants come from
    """

    simple_representation_for_mutants = {}

    #each mutant parent contains a list of mutants
    for mutant in usegraph.hash_mutants:

        #we have now the representation of all mutants children for a parent
        simple_representation_for_mutants[mutant] = computeSimpleRepresentationForAMutant(mutant, usegraph)

    return simple_representation_for_mutants

def getComplexRepresentationForMutants(usegraph):
    """
    Abstract: Method to return a complex representation for mutants : for a mutant father, which mutant (and how much) has failed for a mutant child
    usegraph: The usegraph object which mutants come from
    """

    simple_representation_for_mutants = getSimpleRepresentationForMutants(usegraph)

    complex_representation_for_mutants = {}

    #mutant : {position_of_the_mutation1 : [test1,...], position_of_the_mutation2 : [test1,...]}
    for mutant_list in simple_representation_for_mutants:

        #number of mutants in the hash map is the number of tests
        nb_of_tests = len(usegraph.hash_mutants[mutant_list]['list_mutants'])

        all_tests = {}

        for mutant in simple_representation_for_mutants[mutant_list]:

            #mutants_id is a list which represents id of each mutant
            mutants_id = simple_representation_for_mutants[mutant_list][mutant]

            if usegraph.debug_mode:
                print("mutant {0}".format(mutant))

            #for each mutant id...
            for mutant_id in mutants_id:

                #decrement the nb of tests if the mutant is not in a file test!
                if not mutant_id in usegraph.available_mutants:

                    if usegraph.debug_mode:
                        print("mutant_id {0} not in the list...".format(mutant_id))

                    #if the mutant is not available, the number of tests decreases
                    nb_of_tests = nb_of_tests - 1

                else:
                    if usegraph.debug_mode:
                        print("mutant_id {0} in the list...".format(mutant_id))

                    #store the list of impacted tests
                    impacted_tests = usegraph.mutants[mutant_id]['impacted_tests']

                    #we can work on it if the list is not empty
                    if not len(impacted_tests) == 0:

                        #for each test in the list of impacted tests...
                        for test in impacted_tests:

                            #store his own id
                            test_id = test['id']

                            if not test_id in all_tests:
                                all_tests[test_id] = 0

                            all_tests[test_id] = all_tests[test_id] + 1

                    #only to debug!
                    else:
                        if usegraph.debug_mode:
                            print("no impacted tests for {0}".format(mutant_id))

        #compute the average
        for test in all_tests:
            all_tests[test] = all_tests[test] / nb_of_tests

        #get only usefull representations (the value isn't null...)
        complex_representation_for_mutants[mutant_list] = all_tests

    complex_representation_for_mutants = dict((key, value) for key, value in complex_representation_for_mutants.items() if len(value) != 0)

    return complex_representation_for_mutants

#####################
#LEARNING ALGORITHMS#
#####################

def dichotomicOnlineOptimization(usegraph):
    """
    Abstract: Method to compute probabilities on edges, using a dichotomic approach.\
    The dichotomic approach consists in add the weight of two differents edges (with the same source), and split it into 2.
    usegraph: The usegraph object to compute weights
    """

    begin_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    #Number of batch to compute
    for batch in range(0, usegraph.nb_batch):

        if usegraph.debug_mode:
            need_to_compute_path = 0
            begin_algo = time.time()

        #get the complex representation for each mutant in the usegraph
        complexRepresentation = getComplexRepresentationForMutants(usegraph)

        #reset usefull_edges
        usegraph.usefull_edges = []

        #for each mutant
        for mutant in complexRepresentation:

            #we get the list of test failed
            test_representation = complexRepresentation[mutant]

            #for each test failed
            for test_id in test_representation:

                probability_of_test_id = test_representation[test_id]

                #we look for all fields/methods...
                for node in usegraph.all_cases_id[test_id]['nodes']:

                    id_node = usegraph.all_nodes_id[node]

                    try:

                        #verification node is presents in all paths
                        if not id_node in libs.settings_lib.paths:
                            libs.settings_lib.paths[id_node] = {}

                        #verification mutant is presents in all paths with "node" as source
                        if not mutant in libs.settings_lib.paths[id_node]:
                            libs.settings_lib.paths[id_node][mutant] = []
                            for p in nx.all_simple_paths(usegraph.graph, id_node, mutant):
                                libs.settings_lib.paths[id_node][mutant].append(getExistingPathsFrom(p))
                            if usegraph.debug_mode:
                                need_to_compute_path += 1

                        for one_path in libs.settings_lib.paths[id_node][mutant]:

                            #for each simple path...
                            #transform 'one_path' ([node1, node2, node3, ...] in list of paths [(node1, node2), (node2, node3), ...])
                            simple_path = getExistingPathsFrom(one_path)

                            #for each edge...
                            for edge in one_path:

                                #transform the edge 'id -> (source, target)' as '(source, target) -> id'
                                edge = usegraph.transform_edge_name_as_edge_id(edge)

                                edge_id = usegraph.all_edges_name[edge]['id']

                                if not edge_id in usegraph.usefull_edges:
                                    usegraph.usefull_edges.append(edge_id)

                                source = usegraph.all_edges_id[edge_id]['source']

                                target = usegraph.all_edges_id[edge_id]['target']

                                actual_weight = usegraph.all_weights[usegraph.all_nodes_position_in_weights_matrix[source]][usegraph.all_nodes_position_in_weights_matrix[target]]

                                #update the weight by adding the probability, and / 2
                                usegraph.all_weights[usegraph.all_nodes_position_in_weights_matrix[source]][usegraph.all_nodes_position_in_weights_matrix[target]] = (actual_weight + probability_of_test_id) / 2

                    except:
                        if usegraph.debug_mode:
                            print("ERROR : {0} not found...".format(node))

        if usegraph.debug_mode:
            end_algo = time.time()
            print("Computing time (dichotomicOnlineOptimization) for batch {0}: {1} seconds".format(batch, end_algo - begin_algo))
            print("Need to compute {0} times paths for project {1}".format(need_to_compute_path, usegraph.mutation_operator))

    if "--save_times" in sys.argv:
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        path = "times/{0}.csv".format(usegraph.id.replace('/', '-').replace('.graphml', ''))
        f = open(path, "a")
        f.write("{0} -- {1}\n".format(begin_time, end_time))
        f.close()

def minAndMaxOnlineOptimization(usegraph, f_weight_algo):
    """
    Abstract: Method to compute probabilities on edges, using a 'min and max' algorithm\
    The min and max approach consists in up the minimal weight of edges, if the interesting path is not available (by a random opening).
    usegraph: The usegraph object to compute weights
    """

    for batch in range(1, usegraph.nb_batch + 1):

        if usegraph.debug_mode:
            begin_algo = time.time()
            need_to_compute_path = 0

        complexRepresentation = getComplexRepresentationForMutants(usegraph)

        t = 1

        #reset usefull_edges
        usegraph.usefull_edges = []

        #for each mutant
        for mutant in complexRepresentation:

            #we get the list of test failed
            test_representation = complexRepresentation[mutant]

            #for each test failed
            for test_id in test_representation:

                #we look for all fields/methods...
                for node in usegraph.all_cases_id[test_id]['nodes']:

                    global_probability_to_propagate = 0

                    id_node = usegraph.all_nodes_id[node]

                    try:

                        #verification node is presents in all paths
                        if not id_node in libs.settings_lib.paths:
                            libs.settings_lib.paths[id_node] = {}

                        #verification mutant is presents in all paths with "node" as source
                        if not mutant in libs.settings_lib.paths[id_node]:
                            libs.settings_lib.paths[id_node][mutant] = []
                            for p in nx.all_simple_paths(usegraph.graph, id_node, mutant):
                                libs.settings_lib.paths[id_node][mutant].append(getExistingPathsFrom(p))
                            if debug_mode:
                                need_to_compute_path += 1

                        if len(paths) != 0:

                            for one_path in libs.settings_lib.paths[id_node][mutant]:

                                #for each simple path...
                                #transform 'one_path' ([node1, node2, node3, ...] in list of paths [(node1, node2), (node2, node3), ...])
                                simple_path = getExistingPathsFrom(one_path)

                                probability_of_the_path = 1

                                # compute usefull edges and the probability to propagate
                                for edge in one_path:

                                    edge = usegraph.transform_edge_name_as_edge_id(edge)

                                    edge_id = usegraph.all_edges_name[edge]['id']

                                    #usefull edge if presents
                                    if not edge_id in usegraph.usefull_edges:
                                        usegraph.usefull_edges.append(edge_id)

                                    source = usegraph.all_edges_id[edge_id]['source']

                                    target = usegraph.all_edges_id[edge_id]['target']

                                    actual_weight = usegraph.all_weights[usegraph.all_nodes_position_in_weights_matrix[source]][usegraph.all_nodes_position_in_weights_matrix[target]]

                                    #compute the probability of the path by multiplying the weight of each single path
                                    probability_of_the_path *= actual_weight

                                #compute the sum of products
                                global_probability_to_propagate += probability_of_the_path

                            random_propagation = random.uniform(0, 1)

                            #if random <= global -> OK! Else, we have to up the probability...
                            if not ( random_propagation <= global_probability_to_propagate ):

                                if usegraph.debug_mode:
                                    print("Up {0} due to random_propagation ({1}) > global_probability_to_propagate ({2})".format(edge_id, random_propagation, global_probability_to_propagate))

                                #Get the minimal edge id
                                edge_id = getMinEdgeFrom(paths, usegraph)

                                source = usegraph.all_edges_id[edge_id]['source']

                                target = usegraph.all_edges_id[edge_id]['target']

                                actual_weight = usegraph.all_weights[usegraph.all_nodes_position_in_weights_matrix[source]][usegraph.all_nodes_position_in_weights_matrix[target]]

                                #if the minimal value of the edge is lower than 1...
                                if (actual_weight + f_weight(f_weight_algo, t)) < 1:

                                    #put weight up to the minimal edge
                                    usegraph.all_weights[usegraph.all_nodes_position_in_weights_matrix[source]][usegraph.all_nodes_position_in_weights_matrix[target]] += f_weight(f_weight_algo, t)

                                else:

                                    #put weight to 1 to the minimal edge
                                    usegraph.all_weights[usegraph.all_nodes_position_in_weights_matrix[source]][usegraph.all_nodes_position_in_weights_matrix[target]] = 1

                    except:

                        if usegraph.debug_mode:
                            print("ERROR: {0} not found...".format(node))

                t += 1

        if usegraph.debug_mode:
            end_algo = time.time()
            print("Computing time (minAndMaxOnlineOptimization) for batch {0}: {1} seconds".format(batch, end_algo - begin_algo))
            print("Need to compute {0} times paths for project {1}".format(need_to_compute_path, usegraph.mutation_operator))

def updateAllEdgesOnlineOptimization(usegraph, f_weight_algo):
    """
    Abstract: Method to compute probabilities on edges, using an algorithm which update all edges in a path between source mutation and test
    usegraph: The usegraph object to compute weights
    """

    for batch in range(1, usegraph.nb_batch + 1):

        #print("Batch {0} / {1} for {2}".format(batch, usegraph.nb_batch, usegraph.mutation_operator))

        if usegraph.debug_mode:
            need_to_compute_path = 0
            begin_algo = time.time()

        complexRepresentation = getComplexRepresentationForMutants(usegraph)

        nb_mutants = len(complexRepresentation)

        #reset usefull_edges
        usegraph.usefull_edges = []

        #for each mutant
        for mutant in complexRepresentation:

            #print("Mutant {0}/{1} for {2}... ".format(nb_mutant, len(complexRepresentation), usegraph.mutation_operator), end="")

            #we get the list of test failed
            test_representation = complexRepresentation[mutant]

            #for each test failed
            for test_id in test_representation:

                #we look for all fields/methods...
                for node in usegraph.all_cases_id[test_id]['nodes']:

                    global_probability_to_propagate = 0

                    all_simple_paths = []

                    id_node = usegraph.all_nodes_id[node]

                    try:

                        #verification node is presents in all paths
                        if not id_node in libs.settings_lib.paths:
                            libs.settings_lib.paths[id_node] = {}

                        #verification mutant is presents in all paths with "node" as source
                        if not mutant in libs.settings_lib.paths[id_node]:
                            libs.settings_lib.paths[id_node][mutant] = []
                            for p in nx.all_simple_paths(usegraph.graph, id_node, mutant):
                                libs.settings_lib.paths[id_node][mutant].append(getExistingPathsFrom(p))
                            if usegraph.debug_mode:
                                need_to_compute_path += 1

                        for one_path in libs.settings_lib.paths[id_node][mutant]:

                            probability_of_the_path = 1

                            # compute usefull edges and the probability to propagate
                            for edge in one_path:

                                edge = usegraph.transform_edge_name_as_edge_id(edge)

                                edge_id = usegraph.all_edges_name[edge]['id']

                                #usefull edge if presents
                                if not edge_id in usegraph.usefull_edges:
                                    usegraph.usefull_edges.append(edge_id)

                                #save this to know the simple path to update later...
                                if not edge_id in all_simple_paths:
                                    all_simple_paths.append(edge_id)

                                source = usegraph.all_edges_id[edge_id]['source']

                                target = usegraph.all_edges_id[edge_id]['target']

                                actual_weight = usegraph.all_weights[usegraph.all_nodes_position_in_weights_matrix[source]][usegraph.all_nodes_position_in_weights_matrix[target]]

                                #compute the probability of the path by multiplying the weight of each single path
                                probability_of_the_path *= actual_weight

                            #compute the sum of products
                            global_probability_to_propagate += probability_of_the_path

                        random_propagation = random.uniform(0, 1)

                        #if random <= global -> OK! Else, we have to up the probability...
                        if not ( random_propagation <= global_probability_to_propagate ):

                            if usegraph.debug_mode:
                                print("Up {0}/{1} due to random_propagation ({1}) > global_probability_to_propagate ({2})".format(test_id, node, random_propagation, global_probability_to_propagate))

                            #put weight up to edges

                            for edge_id in all_simple_paths:

                                source = usegraph.all_edges_id[edge_id]['source']

                                target = usegraph.all_edges_id[edge_id]['target']

                                actual_weight = usegraph.all_weights[usegraph.all_nodes_position_in_weights_matrix[source]][usegraph.all_nodes_position_in_weights_matrix[target]]

                                if (actual_weight + f_weight(f_weight_algo, n_batch = batch, nb_mutants = nb_mutants)) < 1:
                                    usegraph.all_weights[usegraph.all_nodes_position_in_weights_matrix[source]][usegraph.all_nodes_position_in_weights_matrix[target]] += f_weight(f_weight_algo, n_batch = batch, nb_mutants = nb_mutants)
                                else:
                                    usegraph.all_weights[usegraph.all_nodes_position_in_weights_matrix[source]][usegraph.all_nodes_position_in_weights_matrix[target]] = 1

                    except:

                        if usegraph.debug_mode:
                            print("ERROR: {0} not found...".format(node))

        if usegraph.debug_mode:
            end_algo = time.time()
            print("Computing time (updateAllEdgesOnlineOptimization) for batch {0}: {1} seconds".format(batch, end_algo - begin_algo))
            print("Need to compute {0} times paths for project {1}".format(need_to_compute_path, usegraph.mutation_operator))

def tagEachUsefullEdgesOptimization(usegraph):
    """
    Abstract: Method to compute the probability to pass from a mutant node to a test node, by giving the probability 1 to each edge in a viable mutant testing
    usegraph: The usegraph object to compute weights
    """

    begin_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    for batch in range(0, usegraph.nb_batch):

        if usegraph.debug_mode:
            need_to_compute_path = 0
            begin_algo = time.time()

        complexRepresentation = getComplexRepresentationForMutants(usegraph)

        #reset usefull_edges
        usegraph.usefull_edges = []

        nb_mutant = 0

        #for each mutant
        for mutant in complexRepresentation:

            #print("mutant {0}/{1} for {2}...".format(nb_mutant, len(complexRepresentation), usegraph.mutation_operator), end="")

            #we get the list of test failed
            test_representation = complexRepresentation[mutant]

            #for each test failed
            for test_id in test_representation:

                #we look for all fields/methods...
                for node in usegraph.all_cases_id[test_id]['nodes']:

                    all_simple_paths = []

                    id_node = usegraph.all_nodes_id[node]

                    try:

                        #verification node is presents in all paths
                        if not id_node in libs.settings_lib.paths:
                            libs.settings_lib.paths[id_node] = {}

                        #verification mutant is presents in all paths with "node" as source
                        if not mutant in libs.settings_lib.paths[id_node]:
                            libs.settings_lib.paths[id_node][mutant] = []
                            for p in nx.all_simple_paths(usegraph.graph, id_node, mutant):
                                libs.settings_lib.paths[id_node][mutant].append(getExistingPathsFrom(p))
                            if usegraph.debug_mode:
                                need_to_compute_path += 1

                        for one_path in libs.settings_lib.paths[id_node][mutant]:

                            #for each simple path...
                            #transform 'one_path' ([node1, node2, node3, ...] in list of paths [(node1, node2), (node2, node3), ...])
                            simple_path = getExistingPathsFrom(one_path)

                            # compute usefull edges and the probability to propagate
                            for edge in one_path:

                                edge = usegraph.transform_edge_name_as_edge_id(edge)

                                edge_id = usegraph.all_edges_name[edge]['id']

                                #usefull edge if presents
                                if not edge_id in usegraph.usefull_edges:
                                    usegraph.usefull_edges.append(edge_id)

                                #save this to know the simple path to update later...
                                if not edge_id in all_simple_paths:
                                    all_simple_paths.append(edge_id)

                                source = usegraph.all_edges_id[edge_id]['source']

                                target = usegraph.all_edges_id[edge_id]['target']

                                usegraph.all_weights[usegraph.all_nodes_position_in_weights_matrix[source]][usegraph.all_nodes_position_in_weights_matrix[target]] = 1
                    except:

                        if usegraph.debug_mode:
                            print("ERROR: {0} not found...".format(node))

            nb_mutant += 1


        if usegraph.debug_mode:
            end_algo = time.time()
            print("Computing time (tagEachUsefullEdgesOptimization) for batch {0}: {1} seconds".format(batch, end_algo - begin_algo))
            print("Need to compute {0} times paths for project {1}".format(need_to_compute_path, usegraph.mutation_operator))

    if "--save_times" in sys.argv:
        end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        path = "times/{0}.csv".format(usegraph.id.replace('/', '-').replace('.graphml', ''))
        f = open(path, "a")
        f.write("{0} -- {1}\n".format(begin_time, end_time))
        f.close()
