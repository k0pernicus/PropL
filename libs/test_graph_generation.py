import random

import networkx as nx

def isEmpty(list):
    """
    Abstract: Function to know if the list (as parameter) is empty or not
    """

    return len(list) == 0

def generate_some_examples(graph):
    """
    Abstract: Function to generate some examples with graph object
    """

    ex_list = []

    for i in range(0, graph.nb_ex):

        source_node = random.choice(graph.graph.nodes())

class GraphPropagation(object):
    """
    Abstract: Class to test propagations of bugs in graphs.
    Graphs are build with an algorithm of Vincenzo Musco.
    """

    def __init__(self, id, nb_nodes, nb_ex):
        self.id = id
        self.nb_nodes = nb_nodes
        self.nb_ex = nb_ex
        self.weights_matrix = {}
        self.graph = self.generate()

    def __del__(self):
        pass

    def run(self):
        self.putLabelsAndInitWeightsMatrix()

    def generate(self):
        """
        Abstract: Function to generate a graph like Vincenzo Musco works
        """

        new_graph_vincenzo = nx.DiGraph()

        # p = random.uniform(0,1)
        #
        # q = random.uniform(0,1)

        p = 0.6

        q = 0.4

        all_nodes = [0,1,2]

        all_edges = [(0,1), (0,2)]

        for i in range(3, self.nb_nodes):
            all_nodes.append(i)
            if random.uniform(0,1) <= p:
                random_node = random.choice(all_nodes)
                while random_node == i:
                    random_node = random.choice(all_nodes)
                all_edges.append((i, random_node))
                children = [child for (source, child) in all_edges if (source == random_node)]
                for child in children:
                    all_edges.append((i, child))
                if random.uniform(0,1) <= q:
                    random_node = random.choice(all_nodes)
                    while random_node == i:
                        random_node = random.choice(all_nodes)
                    all_edges.append((i, random_node))
                    children = [child for (source, child) in all_edges if (source == random_node)]
                    for child in children:
                        all_edges.append((i, child))
            else:
                random_node = random.choice(all_nodes)
                while random_node == i:
                    random_node = random.choice(all_nodes)
                all_edges.append((random_node, i))

        new_graph_vincenzo.add_nodes_from(all_nodes)

        new_graph_vincenzo.add_edges_from(all_edges)

        return new_graph_vincenzo

    def putLabelsAndInitWeightsMatrix(self):
        """
        Abstract: Primitive to label a node, in the self.graph parameter
        """

        for source_node in self.graph.nodes():

            self.weights_matrix[source_node] = {}
            self.weights_matrix[source_node]['visited'] = False

            #add label "target" to each node which is a target of an edge AND which is not already a source
            if len(self.graph.edge[source_node]) == 0:
                self.graph.node[source_node] = "target"

            else:
                #add label "source" to each node which is a source of an edge
                self.graph.node[source_node] = "source"

                nb_of_target_nodes = len(self.graph.edge[source_node])

                self.weights_matrix[source_node][source_node] = 0

                #for each target_node, put the probability to go in the next node to 1/nb_of_target_nodes
                for target_node in self.graph.edge[source_node]:
                    self.weights_matrix[source_node][target_node] = 1/nb_of_target_nodes

    def computeInitNodes(self):
        """
        Abstract: Function to return init nodes in the graph
        """

        init_nodes = []

        for i in range(0, self.nb_nodes):
            init_nodes.append(i)

        #for each target of each edge, replace the number by 0
        for edge in self.graph.edges():
            #avoid recursive functions
            if edge[0] != edge[1]:
                init_nodes[edge[1]] = 0

        return [x for x in init_nodes if x != 0 and len(self.graph.edge[x]) != 0]

    def computeSpecificWeight(self, probability_of_source_edge, source_node, target_node):
        """
        Abstract: Primitive to compute the weight of edges, based on his own propagation probability
        """

        is_target_node_visited = self.weights_matrix[target_node]['visited']

        print("target {0} visited -> {1}".format(target_node, is_target_node_visited))

        if is_target_node_visited:
            self.weights_matrix[source_node][target_node] = (self.weights_matrix[source_node][target_node] + probability_of_source_edge) / 2
        else:
            self.weights_matrix[source_node][target_node] = self.weights_matrix[source_node][target_node] * probability_of_source_edge
            self.weights_matrix[target_node]['visited'] = True

    def computeWeightsMatrix(self):
        """
        Abstract: Primitive to compute the weights matrix
        """

        init_nodes = self.computeInitNodes()

        #for each init node...
        for init_node in init_nodes:

            #create a stock to stock target nodes
            nodes_stack = []

            #for each of those target...
            for target_node in self.graph.edge[init_node]:

                if target_node != 'visited' and self.graph.node[target_node] != "target":

                    nodes_stack.append((target_node, self.weights_matrix[init_node][target_node]))

            while not isEmpty(nodes_stack):

                source_node, probability_of_source_edge = nodes_stack.pop()))

                probability_to_propagate = 0

                for target_node in self.graph.edge[source_node]:

                    if target_node != "visited" and target_node != source_node:

                        self.computeSpecificWeight(probability_of_source_edge, source_node, target_node)

                        probability_to_propagate += self.weights_matrix[source_node][target_node]

                        if self.graph.node[target_node] != "target":

                            nodes_stack.append((target_node, self.weights_matrix[source_node][target_node]))

                probability_to_stay = (1 - probability_to_propagate)

                self.weights_matrix[source_node][source_node] = probability_to_stay
