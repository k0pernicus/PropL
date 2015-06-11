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

    variables_table = []

    methods_table = []

    for node in use_graph.nodes():
        if not node in (item[0] for item in use_graph.edges()):
            variables_table.append(node)
        else:
            methods_table.append(node)

    for variable_label in variables_table:
        use_graph.node[variable_label]['type'] = "VARIABLE"

    for method_label in methods_table:
        use_graph.node[method_label]['type'] = "METHOD"

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
        use_graph.edge[source][target]['weight'] = random.uniform(0,1)

def generate_new_example(use_graph):
    """
    Abstract: Generate a new example of graph with propagations from one mutant
    Return this one
    """

    source_node = random.choice(use_graph.nodes())

    impacted_nodes = []

    interested_nodes = []

    interested_edges = []

    impacted_nodes.append(source_node)

    interested_nodes.append((source_node, use_graph.node[source_node]['type']))

    while len(impacted_nodes) != 0:
        source_studied = impacted_nodes.pop(0)
        for edge in use_graph.edges_iter():
            source_of_edge, target_of_edge = edge
            if (source_studied == target_of_edge) and (use_graph.edge[source_of_edge][target_of_edge]['weight'] >= 0.5):
                interested_edges.append((edge, use_graph.edge[source_of_edge][target_of_edge]['type']))
                if not source_of_edge in impacted_nodes:
                    impacted_nodes.append(source_of_edge)
                    interested_nodes.append((source_of_edge, use_graph.node[source_node]['type']))

    new_exemple = nx.DiGraph()

    for node in interested_nodes:
        node_name, node_type = node
        new_example.add_node(node_name, type=node_type)

    for edge in interested_edges:
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
