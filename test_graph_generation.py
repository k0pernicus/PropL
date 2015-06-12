import networkx as nx
import matplotlib.pyplot as plt
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

def generate_new_example(use_graph, first_sources = []):
    """
    Abstract: Generate a new example of graph with propagations from one mutant
    Return this one
    """

    #stack to know impacted nodes
    impacted_nodes = []

    source_node = random.choice(use_graph.nodes())

    #add a random node in the list of impacted nodes
    impacted_nodes.append(source_node)

    print("source_node: {0}".format(source_node))

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
            if (source_studying == target_of_edge) and ((random.randint(1, 10) / 10) <= use_graph.edge[source_of_edge][target_of_edge]['weight']):
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

def visualize(graph):
    """
    Abstract: Function to visualize the graph
    """

    pos=nx.spring_layout(graph)

    blue_nodes = [id_node for id_node, type_node in graph.nodes(data = True) if (type_node['fillcolor'] == 'blue') and (type_node['type'] == 'METHOD')]

    green_nodes = [id_node for id_node, type_node in graph.nodes(data = True) if (type_node['fillcolor'] == 'blue') and (type_node['type'] == 'VARIABLE')]

    red_node = [id_node for id_node, type_node in graph.nodes(data = True) if type_node['fillcolor'] == 'red']

    nx.draw_networkx_nodes(graph, pos, red_node, alpha=0.5, node_color = 'r', label = red_node, with_label = True)

    nx.draw_networkx_nodes(graph, pos, blue_nodes, alpha=0.5, node_color = 'b', label = blue_nodes, with_label = True)

    nx.draw_networkx_nodes(graph, pos, green_nodes, alpha=0.5, node_color = 'g', label = green_nodes, with_label = True)

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
