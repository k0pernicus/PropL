import networkx as nx
import math
import random

def getMinEdgeFrom(paths, usegraph):
    """
    Abstract: Function to return the id of the edge which have the minimal weight
    """

    min = 1

    edge_id = ''

    for all_paths in paths:

        all_paths = getExistingPathsFrom(all_paths)

        for p in all_paths:

            edge = usegraph.transform_edge_name_as_edge_id(p)
            edge_id_tmp = usegraph.all_edges_name[edge]['id']
            edge_weight = usegraph.all_edges_id[edge_id_tmp]['weight']
            if edge_weight <= min:
                min = edge_weight
                edge_id = edge_id_tmp

    return edge_id

def getExistingPathsFrom(all_paths):
    """
    Abstract: Function to transform the list of nodes (all_paths) to a list of tuples (source, target)
    """

    return [(all_paths[a], all_paths[a + 1]) for a in range(0, len(all_paths) - 1)]

def computeSimpleRepresentationForAMutant(mutant, usegraph):
    """
    Abstract: Method to return a simple representation for one mutant
    Parameters are the mutant to study and the UseGraph object which the mutant come from
    """

    simple_representation_by_mutant = {}

    #searching for all mutant id in the list of mutants
    for single_mutant_id in usegraph.hash_mutants[mutant]['list_mutants']:

        #this field is a tag to know if there's multiple tests for the same mutation
        position_of_the_mutation = "{0}||{1}".format(usegraph.mutants[single_mutant_id]['from'], usegraph.mutants[single_mutant_id]['to'])

        if not position_of_the_mutation in simple_representation_by_mutant:
            simple_representation_by_mutant[position_of_the_mutation] = []

        simple_representation_by_mutant[position_of_the_mutation].append(single_mutant_id)

    return simple_representation_by_mutant

def getSimpleRepresentationForMutants(usegraph):
    """
    Abstract: Method to return a representation of which mutant is the child of a father mutant
    The parameter is a UseGraph object
    """

    simple_representation_for_mutants = {}

    #each mutant parent contains a list of mutants
    for mutant in usegraph.hash_mutants:

        #we have now the representation of all mutants children for a parent
        simple_representation_for_mutants[mutant] = computeSimpleRepresentationForAMutant(mutant, usegraph)

    return simple_representation_for_mutants

def getComplexRepresentationForMutants(usegraph):
    """
    Abstract: Method to return a complex representation for mutants : for a mutant father, which mutant (and how much) has been failed for a mutant child
    The parameter is a UseGraph object
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

def dichotomicOnlineOptimization(usegraph):
    """
    Abstract: Method to compute probabilities on edges, using a dichotomic approach
    The parameter is a UseGraph object
    """

    if usegraph.debug_mode:
        begin_algo = time.time()

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

                paths = []

                for p in nx.all_simple_paths(usegraph.graph, usegraph.all_nodes_id[node], mutant):
                    paths.append(p)

                for one_path in paths:

                    #for each simple path...
                    #transform 'one_path' ([node1, node2, node3, ...] in list of paths [(node1, node2), (node2, node3), ...])
                    simple_path = getExistingPathsFrom(one_path)

                    #for each edge...
                    for edge in simple_path:

                        #transform the edge 'id -> (source, target)' as '(source, target) -> id'
                        edge = usegraph.transform_edge_name_as_edge_id(edge)

                        edge_id = usegraph.all_edges_name[edge]['id']

                        if not edge_id in usegraph.usefull_edges:
                            usegraph.usefull_edges.append(edge_id)

                        #update the weight by adding the probability, and / 2
                        usegraph.all_edges_id[edge_id]['weight'] = (usegraph.all_edges_id[edge_id]['weight'] + probability_of_test_id) / 2

    if usegraph.debug_mode:
        end_algo = time.time()

    if usegraph.debug_mode:
        print("Computing time (dichotomicOnlineOptimization) : {0} seconds".format(end_algo - begin_algo))

def minAndMaxOnlineOptimization(usegraph):
    """
    Abstract: Method to compute probabilities on edges, using a 'min and max' algorithm
    The parameter is a UseGraph object
    """

    if usegraph.debug_mode:
        begin_algo = time.time()

    complexRepresentation = getComplexRepresentationForMutants(usegraph)

    t = 1000

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

                paths = []

                for p in nx.all_simple_paths(usegraph.graph, usegraph.all_nodes_id[node], mutant):
                    paths.append(p)

                for one_path in paths:

                    #for each simple path...
                    #transform 'one_path' ([node1, node2, node3, ...] in list of paths [(node1, node2), (node2, node3), ...])
                    simple_path = getExistingPathsFrom(one_path)

                    probability_of_the_path = 1

                    # compute usefull edges and the probability to propagate
                    for edge in simple_path:

                        edge = usegraph.transform_edge_name_as_edge_id(edge)

                        edge_id = usegraph.all_edges_name[edge]['id']

                        #usefull edge if presents
                        if not edge_id in usegraph.usefull_edges:
                            usegraph.usefull_edges.append(edge_id)

                        #compute the probability of the path by multiplying the weight of each single path
                        probability_of_the_path *= usegraph.all_edges_id[edge_id]['weight']

                    #compute the sum of products
                    global_probability_to_propagate += probability_of_the_path

                random_propagation = random.uniform(0, 1)

                #if random <= global -> OK! Else, we have to up the probability...
                if not ( random_propagation <= global_probability_to_propagate ) and ( usegraph.all_edges_id[edge_id]['weight'] < 1 ):

                    #Get the minimal edge id
                    edge_id = getMinEdgeFrom(paths, usegraph)

                    if usegraph.debug_mode:
                        print("Up {0} due to random_propagation ({1}) > global_probability_to_propagate ({2})".format(edge_id, random_propagation, global_probability_to_propagate))

                    #up the weight of this edge
                    usegraph.all_edges_id[edge_id]['weight'] += (1 / math.log(t))

                    if usegraph.all_edges_id[edge_id]['weight'] > 1:
                        usegraph.all_edges_id[edge_id]['weight'] = 1

        t += 1

    if usegraph.debug_mode:
        end_algo = time.time()

    if usegraph.debug_mode:
        print("Computing time (minAndMaxOnlineOptimization) : {0} seconds".format(end_algo - begin_algo))

def updateAllEdgesOnlineOptimization(usegraph):
    """
    Abstract: Method to compute probabilities on edges, using an algorithm which update all edges in a path between source mutation and test
    The parameter is a UseGraph object
    """

    if usegraph.debug_mode:
        begin_algo = time.time()

    #ALGO

    if usegraph.debug_mode:
        end_algo = time.time()

    if usegraph.debug_mode:
        print("Computing time (updateAllEdgesOnlineOptimization) : {0} seconds".format(end_algo - begin_algo))

def constraintsBatchOptimization(usegraph):
    """
    Abstract: Method to compute probabilities on edges, using an algorithm which compute each weight as a constraint between paths
    M -> t1 : p1 + p2 + p6 + p9 + p10 ~ proportions
    M'-> t1 : p1 + p3 + p4 + p5 + p9 ~ proportions
    M''->t2 : p10 + p12 ~ proportions...
    """

    if usegraph.debug_mode:
        begin_algo = time.time()

    #ALGO

    if usegraph.debug_mode:
        end_algo = time.time()

    if usegraph.debug_mode:
        print("Computing time (constraintsBatchOptimization) : {0} seconds".format(end_algo - begin_algo))
