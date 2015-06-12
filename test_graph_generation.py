import networkx as nx
import random

def main():
    """
    Abstract: Random generation of use graphs
    """

    generate_random_graph()

def generate_random_graph(nodes, degree):
    """
    Abstract: Function to generate a random graph
    The graph is generated with Barabasi concepts (preferencial attachment), labels and probabilities (to each edges) are added
    Return the generated graph
    """

    new_graph = nx.barabasi_albert_graph(nodes, degree)
    add_labels(new_graph)
    add_probabilities(new_graph)

    return new_graph

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

def add_probabilities(use_graph):
    """
    Abstract: Add random probabilities to edges
    """

    for edge in use_graph.edges_iter():
        source, target = edge
        #random probability with random.uniform
        use_graph.edge[source][target]['weight'] = (random.randint(1, 100) / 100)

def is_algorithm_good_between(use_graph, examples):
    """
    Abstract: Function to match use_graph and examples
    """

    rpb = resolve_pb(examples)

    for edge in use_graph.edges(data = True):
        source, target, data = edge
        edge_st = (source, target)
        if edge_st in rpb:
            print("{0} : {1} - {2}".format((source, target), data['weight'], rpb[edge_st]['weight']))
        else:
            print("{0} : {1} - 0".format((source, target), data['weight']))

def resolve_pb(examples):
    """
    Abstract: Function to resolve the following problem -> to compute efficiently probabilities from examples (compared with the original use graph)
    """

    all_weight = {}

    number_runs = len(examples)

    for ex_graph in examples:
        ex_graph_nodes = ex_graph.nodes()
        ex_graph_edges = ex_graph.edges()

        for edge in ex_graph_edges:
            if not edge in all_weight:
                all_weight[edge] = {'weight' : 1}
            else:
                weight_of_edge = all_weight[edge]['weight']
                all_weight[edge]['weight'] = weight_of_edge + 1

    for edge, weight in all_weight.items():
        all_weight[edge]['weight'] = weight['weight'] / number_runs

    return all_weight

def predict_impacts(use_graph, node):
    """
    Abstract: Algorithm to compute the route from 'node' to others nodes which are impacts of these node
    """

    pass

def generate_new_example(use_graph):
    """
    Abstract: Generate a new example of graph with propagations from one mutant
    Return this one
    """

    source_node = random.choice(use_graph.nodes())

    print("source_node: {0}".format(source_node))

    #stack to know impacted nodes
    impacted_nodes = []

    #list of interesting nodes
    interesting_nodes = []

    #list of interesting edges
    interesting_edges = []

    impacted_nodes.append(source_node)

    interesting_nodes.append((source_node, use_graph.node[source_node]['type'], "source"))

    while len(impacted_nodes) != 0:
        #pop the first impacted node
        source_studied = impacted_nodes.pop(0)

        for edge in use_graph.edges():
            source_of_edge, target_of_edge = edge
            #if the source is the target of an edge, and if the weight is >= 0.5...
            #TODO : weight >= 0.5 which weight is max of weights!!!
            if (source_studied == target_of_edge) and ((random.randint(1, 100) / 100) < use_graph.edge[source_of_edge][target_of_edge]['weight']):
                #the source is interesting!!
                interesting_edges.append((edge, use_graph.edge[source_of_edge][target_of_edge]['type']))
                #if the source is not already in the stack...
                if not source_of_edge in impacted_nodes:
                    #we add it!
                    impacted_nodes.append(source_of_edge)
                    #and we add it to the interesting nodes list
                    interesting_nodes.append((source_of_edge, use_graph.node[source_of_edge]['type'], "none"))

    #new directed graph (the example)
    new_example = nx.DiGraph()

    #each node is added
    for node in interesting_nodes:
        node_name, node_type, source_or_not = node
        if source_or_not == "source":
            new_example.add_node(node_name, type=node_type, fillcolor='red')
        else:
            new_example.add_node(node_name, type=node_type, fillcolor='blue')

    #the same for each edge
    for edge in interesting_edges:
        edge_name, edge_type = edge
        edge_source, edge_target = edge_name
        new_example.add_edge(edge_source, edge_target, type=edge_type)

    return new_example

def generate_some_examples(use_graph, number_of_exemples):
    """
    Abstract: Generate some examples to study the propagation of bugs
    This function will take a random node and considers him like a mutant node
    Return a list which contains number_of_exemples graphs
    """

    new_examples = []

    for i in range(0, number_of_exemples - 1):
        new_examples.append(generate_new_example(use_graph))

    return new_examples

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

if __name__ == "__main__":
    
    main()
