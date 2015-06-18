import networkx as nx
import matplotlib.pyplot as plt
import random
import math

from threading import Thread

def test_graph():

    use_graph = nx.DiGraph()

    use_graph.add_nodes_from([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])

    use_graph.add_edge(0, 1, weight = 0.2)
    use_graph.add_edge(0, 2, weight = 0.5)
    use_graph.add_edge(0, 3, weight = 0.7)
    use_graph.add_edge(1, 4, weight = 0.2)
    use_graph.add_edge(1, 5, weight = 0.4)
    use_graph.add_edge(2, 5, weight = 0.7)
    use_graph.add_edge(3, 7, weight = 0.9)
    use_graph.add_edge(3, 6, weight = 0.9)
    use_graph.add_edge(2, 6, weight = 0.8)
    use_graph.add_edge(5, 6, weight = 0.6)
    use_graph.add_edge(4, 8, weight = 0.7)
    use_graph.add_edge(8, 11, weight = 0.9)
    use_graph.add_edge(8, 12, weight = 0.7)
    use_graph.add_edge(11, 14, weight = 0.2)
    use_graph.add_edge(12, 14, weight = 0.4)
    use_graph.add_edge(14, 17, weight = 0.9)
    use_graph.add_edge(6, 9, weight = 0.3)
    use_graph.add_edge(9, 17, weight = 0.4)
    use_graph.add_edge(7, 10, weight = 0.5)
    use_graph.add_edge(10, 13, weight = 0.1)
    use_graph.add_edge(13, 15, weight = 0.8)
    use_graph.add_edge(13, 16, weight = 0.2)
    use_graph.add_edge(16, 18, weight = 0.2)

    return use_graph

def run_tests(nb, use_graph, examples, weights):
    for i in range(0, nb):
        print("{0} with source {1}".format(examples[i], examples[i]['source']))
        weights = resolve_pb_stoch(use_graph, examples[i], weights)
        is_algorithm_good_between_weights(use_graph, weights)
        input()

def generate_graph_vincenzo(nodes):
    """
    Abstract: Function to generate a graph like Vincenzo works
    """

    new_graph_vincenzo = nx.DiGraph()

    # p = random.uniform(0,1)
    #
    # q = random.uniform(0,1)

    p = 0.6

    q = 0.4

    all_nodes = [0,1,2]

    all_edges = []

    for i in range(3, nodes):
        all_nodes.append(i)
        if random.uniform(0,1) <= p:
            random_node = random.choice(all_nodes)
            all_edges.append((i, random_node))
            children = [child for (source, child) in all_edges if (source == random_node)]
            for child in children:
                all_edges.append((i, child))
            if random.uniform(0,1) <= q:
                random_node = random.choice(all_nodes)
                all_edges.append((i, random_node))
                children = [child for (source, child) in all_edges if (source == random_node)]
                for child in children:
                    all_edges.append((i, child))
        else:
            all_edges.append((random.choice(all_nodes), i))

    new_graph_vincenzo.add_nodes_from(all_nodes)

    new_graph_vincenzo.add_edges_from(all_edges)

    return new_graph_vincenzo

def generate_random_graphs(nodes, degree):
    """
    Abstract: Function to generate a random graph
    The graph is generated with Barabasi concepts (preferencial attachment), labels and probabilities (to each edges) are added
    Return the generated graph
    """

    #Barabasi graph

    new_graph_barabasi = nx.barabasi_albert_graph(nodes, degree)
    add_labels(new_graph_barabasi)
    add_probabilities(new_graph_barabasi)

    #Use graph

    new_graph_vincenzo = generate_graph_vincenzo(nodes)
    add_labels(new_graph_vincenzo)
    add_probabilities(new_graph_vincenzo)

    return (new_graph_barabasi, new_graph_vincenzo)

def add_labels(use_graph):
    """
    Abstract: Add labels to nodes ("METHOD" or "VARIABLE") and to edges ("METHOD_CALL" or "OPERATION")
    """

    #nodes as variables
    variables_table = []

    #nodes as methods
    methods_table = []

    #classification : variables / methods
    for node in use_graph.nodes():
        if not node in (item[0] for item in use_graph.edges()):
            variables_table.append(node)
        else:
            methods_table.append(node)

    for variable_label in variables_table:
        use_graph.node[variable_label]['type'] = "VARIABLE"

    for method_label in methods_table:
        use_graph.node[method_label]['type'] = "METHOD"

    #classification : method call (method -> method) / operation (method -> variable)
    for edge in use_graph.edges_iter():
        source, target = edge
        if (use_graph.node[source]['type'] == "METHOD") and (use_graph.node[target]['type'] == "METHOD"):
            use_graph.edge[source][target]['type'] = "METHOD_CALL"
        else:
            use_graph.edge[source][target]['type'] = "OPERATION"

def get_first_sources(use_graph):
    """
    Abstract: Add labels to first sources in the use graph (first source is a source which is not a target already)
    """

    first_sources = use_graph.nodes()

    for edge in use_graph.edges_iter():
        _, target = edge

        if target in first_sources:
            first_sources.remove(target)

    #we got our first sources...

    return first_sources

def add_probabilities(use_graph):
    """
    Abstract: Add random probabilities to edges
    """

    for edge in use_graph.edges_iter():
        source, target = edge
        #random probability with random.uniform
        use_graph.edge[source][target]['weight'] = (random.randint(1, 10) / 10)

def is_algorithm_good_between_weights(use_graph, weights):
    """
    Abstract: Function to match use_graph and examples weights
    """

    test_ok = 0

    tests = 0

    for weight_item in weights.items():
        edge, weight = weight_item
        weight_of_original_edge = use_graph.edge[edge[0]][edge[1]]['weight']
        if (weight == weight_of_original_edge) or ((weight + 0.1) == weight_of_original_edge) or ((weight - 0.1) == weight_of_original_edge):
            test_ok = test_ok + 1
        print("{0} : {1} / {2}".format(edge, weight, weight_of_original_edge))
        tests = tests + 1

    print("{0} tests ok / {1} tests".format(test_ok, tests))

def is_algorithm_good_between_examples(examples, tests):

    number_of_tests = len(tests)

    good = 0

    fp = 0

    fn = 0

    for i in range(0, number_of_tests):
        if examples[i]['impacted_nodes'] == tests[i]['impacted_nodes']:
            good = good + 1
        # else:
        #     print("Bad {0}".format(tests[i]['impacted_nodes']))

    print("{0}/{1} good!".format(good, number_of_tests))

def resolve_pb_stoch(use_graph, example, paths_weight, first_sources = []):
    """
    Abstract: Function to resolve the following problem -> to compute efficiently probabilities from examples (compared with the original use graph)
    """

    #use_graph transform (in digraph) for the all_simple_paths algorithm...
    di_use_graph = nx.DiGraph()
    di_use_graph.add_nodes_from(use_graph.nodes())
    di_use_graph.add_edges_from(use_graph.edges())

    if len(first_sources) == 0:
        first_sources = get_first_sources(di_use_graph)

    i = 0

    #store the mutation source
    mutation_source = example['source']

    #for each first source (test)...
    for first_source in first_sources:

        all_paths_existing = []

        #we store each path!
        #all_paths = nx.all_simple_paths(di_use_graph, mutation_source, first_source)
        all_paths = nx.all_simple_paths(di_use_graph, first_source, mutation_source)

        #transform the list of nodes to a list of tuples
        for path in all_paths:
            all_paths_existing.append(get_existing_paths_from(path))

        #update the weights table -> is path existing?
        paths_weight = update_weights_table(all_paths_existing, paths_weight)

        #SIMPLE LEARNING algorithm
        #For the example, we will simulate all paths...
        #If a path is ok (we access to the test node) while he shouldn't, we reduce the max probability of a simple path - the inverse is also ok

        #get the path from mutation_source to first_source
        #if the path is ok and in the example not -> put weight down to the high simple path
        #if the path is not ok and in the example it is -> put weight up to the high simple path
        #if ok, continue...

        path_exists = example['impacted_nodes'][first_source]

        test_path = exists_a_path_for_test(all_paths_existing, paths_weight)

        print("test_path: {0}".format(test_path))

        if(not path_exists == test_path):
            #if there is a path from mutation_source to the first_source studying...
            if path_exists:
                up_weight(all_paths_existing, paths_weight)
            #if there is no path...
            else:
                down_weight(all_paths_existing, paths_weight)

        # End of solution 2

        i = i + 1

    return paths_weight

def resolve_pb(use_graph, examples, paths_weight = {}, first_sources = []):
    """
    Abstract: Function to resolve the following problem -> to compute efficiently probabilities from examples (compared with the original use graph)
    """

    #use_graph transform (in digraph) for the all_simple_paths algorithm...
    di_use_graph = nx.DiGraph()
    di_use_graph.add_nodes_from(use_graph.nodes())
    di_use_graph.add_edges_from(use_graph.edges())

    if len(first_sources) == 0:
        first_sources = get_first_sources(di_use_graph)

    i = 1

    all = len(examples) - 1

    #for each example...
    for example in examples:

        print("{0}/{1} : {2}".format(i, all, example))

        #store the mutation source
        mutation_source = example['source']

        #for each first source (test)...
        for first_source in first_sources:

            all_paths_existing = []

            #we store each path!
            #all_paths = nx.all_simple_paths(di_use_graph, mutation_source, first_source)
            all_paths = nx.all_simple_paths(di_use_graph, first_source, mutation_source)
            #transform the list of nodes to a list of tuples
            for path in all_paths:
                all_paths_existing.append(get_existing_paths_from(path))

            #update the weights table -> is path existing?
            paths_weight = update_weights_table(all_paths_existing, paths_weight)

            #SIMPLE LEARNING algorithm
            #For the example, we will simulate all paths...
            #If a path is ok (we access to the test node) while he shouldn't, we reduce the max probability of a simple path - the inverse is also ok

            #get the path from mutation_source to first_source
            #if the path is ok and in the example not -> put weight down to the high simple path
            #if the path is not ok and in the example it is -> put weight up to the high simple path
            #if ok, continue...

            path_exists = example['impacted_nodes'][first_source]

            #test_path = exists_a_path_for_test(all_paths_existing, paths_weight)
            test_path = exists_a_path_for_test_with_max(all_paths_existing, paths_weight)

            if(not path_exists == test_path):
                #if there is a path from mutation_source to the first_source studying...
                if path_exists:
                    up_weight(all_paths_existing, paths_weight, i)
                    #up_weight_min(all_paths_existing, paths_weight, i)
                #if there is no path...
                else:
                    down_weight(all_paths_existing, paths_weight, i)
                    #down_weight_max(all_paths_existing, paths_weight, i)
        i = i + 1

    return paths_weight

def exists_a_path_for_test(paths, weights):
    """
    Abstract: Function to know if a path exists between mutation_source to target
    Return a boolean : True if the path exists, else False
    """

    return (random.uniform(0, 1) < get_weight_by_path(paths, weights))

def get_product_of_simple_paths(path, paths_weight):

    simple_path_weight = 1

    for simple_path in path:

        simple_path_weight = simple_path_weight * paths_weight[simple_path]

    return simple_path_weight

def exists_a_path_for_test_with_max(paths, weights):

    rand = random.uniform(0,1)

    for path in paths:
        if rand < get_product_of_simple_paths(path, weights):
            return True

    return False

def get_existing_paths_from(all_paths):
    """
    Abstract: Function to transform the list of nodes (all_paths) to a list of tuples (source, target)
    """

    return [(all_paths[a], all_paths[a + 1]) for a in range(0, len(all_paths) - 1)]

def update_weights_table(all_paths_existing, paths_weight):
    """
    Abstract: Update the weights table with new path from 'all_paths_existing'
    """

    for path in all_paths_existing:
        for simple_path in path:
            #if the simple path doesn't exists in the table, we create it with a probability equals to 0.1
            if not simple_path in paths_weight:
                paths_weight[simple_path] = round(0.5, 10)

    return paths_weight

def get_weight_by_path(all_paths_existing, paths_weight):
    """
    Abstract: Get global weight for all path
    """

    global_path_weight = 0

    #for each path...
    for path in all_paths_existing:

        simple_path_weight = 1

        #for each simple path...
        for simple_path in path:

            simple_path_weight = simple_path_weight * paths_weight[simple_path]

        global_path_weight = global_path_weight + simple_path_weight

    return global_path_weight

def up_weight(all_paths_existing, paths_weight, t):
    """
    Abstract: Function to up the minimal weight of the simple path...
    """

    all_simple_paths = {}

    for path in all_paths_existing:
        for simple_path in path:
            if not simple_path in all_simple_paths:
                all_simple_paths[simple_path] = False

    for path in all_paths_existing:
        for simple_path in path:
            if paths_weight[simple_path] < 1 and (all_simple_paths[simple_path] == False):
                #paths_weight[simple_path] = round(paths_weight[simple_path] + 0.1, 10)
                try:
                    paths_weight[simple_path] = paths_weight[simple_path] + (1 / math.log(t))
                except:
                    paths_weight[simple_path] = paths_weight[simple_path] + 0.5
                all_simple_paths[simple_path] = True

def down_weight(all_paths_existing, paths_weight, t):
    """
    Abstract: Function to down the maximal weight of the simple path...
    """

    all_simple_paths = {}

    for path in all_paths_existing:
        for simple_path in path:
            if not simple_path in all_simple_paths:
                all_simple_paths[simple_path] = False

    for path in all_paths_existing:
        for simple_path in path:
            if paths_weight[simple_path] > 0.1 and (all_simple_paths[simple_path] == False):
                #paths_weight[simple_path] = round(paths_weight[simple_path] - 0.1, 10)
                try:
                    paths_weight[simple_path] = paths_weight[simple_path] - (1 / math.log(t))
                except:
                    paths_weight[simple_path] = paths_weight[simple_path] - 0.5
                all_simple_paths[simple_path] = True

def up_weight_min(all_paths_existing, paths_weight, t):
    """
    Abstract: Function to up the minimal weight of the simple path...
    """

    simple_paths = []

    #merge all path
    for path in all_paths_existing:
        simple_paths + path

    minimum_path = min(paths_weight, key=paths_weight.get)
    minimum_weight = paths_weight[minimum_path]

    if minimum_weight < 1:
        try:
            paths_weight[minimum_path] = minimum_weight + (1 / math.log(t))
        except:
            paths_weight[minimum_path] = minimum_weight + (1 / math.log(t + 1))

def down_weight_max(all_paths_existing, paths_weight, t):
    """
    Abstract: Function to down the maximal weight of the simple path...
    """

    simple_paths = []

    #merge all path
    for path in all_paths_existing:
        simple_paths + path

    maximum_path = max(paths_weight, key=paths_weight.get)
    maximum_weight = paths_weight[maximum_path]

    if maximum_weight > 0.1:
        try:
            paths_weight[maximum_path] = maximum_weight - (1 / math.log(t))
        except:
            paths_weight[maximum_path] = maximum_weight - (1 / math.log(t + 1))

def generate_new_example(use_graph, first_sources = [], source_node = 0):
    """
    Abstract: Generate a new example of graph with propagations from one mutant
    Return this one
    """

    #stack to know impacted nodes
    impacted_nodes = []

    all_nodes = []

    if source_node == 0:
        source_node = random.choice(use_graph.nodes())
        while source_node in first_sources:
            source_node = random.choice(use_graph.nodes())

    #add a random node in the list of impacted nodes
    impacted_nodes.append(source_node)

    if len(first_sources) == 0:
        first_sources = get_first_sources(use_graph)

    #dictionary which give us the information : "Does a final source impacted?"
    impacted_final_sources = {}

    #false (concerning the impact) to all first sources
    for source in first_sources:
        impacted_final_sources[source] = False

    while len(impacted_nodes) != 0:
        #pop the first impacted node
        source_studying = impacted_nodes.pop(0)

        for edge in use_graph.edges():
            source_of_edge, target_of_edge = edge
            #if the source is the target of an edge, and if the weight is >= 0.5...
            #TODO : weight >= 0.5 which weight is max of weights!!!
            if (source_studying == target_of_edge) and (round((random.randint(1, 10) / 10), 10) <= use_graph.edge[source_of_edge][target_of_edge]['weight']):
                #the source is interesting!!
                #if the source is part of impacted_final_sources, we change the boolean to True (because we have visited it)
                if source_of_edge in impacted_final_sources:
                    impacted_final_sources[source_of_edge] = True
                #else...
                else:
                    #we add it to the list of impacted nodes if he's not already in...
                    if not source_of_edge in impacted_nodes:
                        #if is not already in, we add it!
                        impacted_nodes.append(source_of_edge)

    return {'source' : source_node, 'impacted_nodes' : impacted_final_sources}

def do_tests(nb, nb_ex, use_graph, weights):
    for i in range(0, nb):
        examples_training = generate_some_examples(use_graph, nb_ex)
        tests = generate_some_tests(use_graph, examples_training, weights, len(examples_training))
        is_algorithm_good_between_examples(examples_training, tests)

def generate_some_examples(use_graph, number_of_exemples):
    """
    Abstract: Generate some examples to study the propagation of bugs
    This function will take a random node and considers him like a mutant node
    Return a list which contains number_of_exemples graphs
    """

    new_examples = []

    first_sources = get_first_sources(use_graph)

    nb_sources = len(first_sources)

    for i in range(0, number_of_exemples):

        node = random.randint(nb_sources, use_graph.number_of_nodes() - 1)

        ex = generate_new_example(use_graph, first_sources, node)

        new_examples.append(ex)

    return new_examples

def generate_some_tests(use_graph, examples, weights, number_of_exemples):

    tests = []

    for i in range(0, number_of_exemples - 2):
        # t = Thread(target=generate_new_test, args=(use_graph, weights, examples[i]['source'],)).start()
        # tests.append(t)

        tests.append(generate_new_test(use_graph, weights, examples[i]['source']))

    return tests

def generate_new_test(use_graph, weights, source_node):

    #stack to know impacted nodes
    impacted_nodes = []

    #add a random node in the list of impacted nodes
    impacted_nodes.append(source_node)

    first_sources = get_first_sources(use_graph)

    #dictionary which give us the information : "Does a final source impacted?"
    impacted_final_sources = {}

    #false (concerning the impact) to all first sources
    for source in first_sources:
        impacted_final_sources[source] = False

    while len(impacted_nodes) != 0:
        #pop the first impacted node
        source_studying = impacted_nodes.pop(0)

        for edge in use_graph.edges():
            source_of_edge, target_of_edge = edge
            if not edge in weights:
                weights[edge] = 0.5
            #if the source is the target of an edge, and if the weight is >= 0.5...
            #TODO : weight >= 0.5 which weight is max of weights!!!
            if (source_studying == target_of_edge) and ((random.randint(1, 10) / 10) <= weights[(source_of_edge,target_of_edge)]):
                #the source is interesting!!
                #if the source is part of impacted_final_sources, we change the boolean to True (because we have visited it)
                if source_of_edge in impacted_final_sources:
                    impacted_final_sources[source_of_edge] = True
                #else...
                else:
                    #we add it to the list of impacted nodes if he's not already in...
                    if not source_of_edge in impacted_nodes:
                        #if is not already in, we add it!
                        impacted_nodes.append(source_of_edge)

    return {'source' : source_node, 'impacted_nodes' : impacted_final_sources}

def write_basic_usegraph(graph):
    """
    Abstract: Function to write the graph as graphml
    """

    nx.write_graphml(graph, "tests/graph_generation/usegraph.graphml")

def write_usegraph_examples(graphs):
    """
    Abstract: Function to write each usegraph example as graphml
    """

    i = 0

    for graph in graphs:
        nx.write_graphml(graph, "tests/graph_generation/graph_ex{0}.graphml")
        i = i + 1

def visualize(graph, first_sources = []):
    """
    Abstract: Function to visualize the graph
    """

    if len(first_sources) == 0:
        first_sources = get_first_sources(graph)

    pos=nx.spring_layout(graph)

    blue_nodes = [id_node for id_node, type_node in graph.nodes() if not id_node in first_sources]

    red_node = [id_node for id_node, type_node in graph.nodes() if id_node in first_sources]

    nx.draw_networkx_nodes(graph, pos, red_node, alpha=0.5, node_color = 'r', label = red_node, with_label = True)

    nx.draw_networkx_nodes(graph, pos, blue_nodes, alpha=0.5, node_color = 'b', label = blue_nodes, with_label = True)

    nx.draw_networkx_edges(graph, pos, graph.edges(), alpha=0.5, width=1.0)

    labels={}

    labels_node = graph.nodes()

    for i in range(0, len(labels_node)):
        labels[labels_node[i]] = labels_node[i]
        #print("label {0} : {1}".format(i, labels[i]))

    nx.draw_networkx_labels(graph, pos, labels, font_size=16)

    plt.show()


if __name__ == "__main__":

    main()