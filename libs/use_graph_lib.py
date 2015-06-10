import os
import time

import networkx as nx
import matplotlib.pyplot as plt

class UseGraph(object):
    """
    Abstract: Class which represents a use graph.
    A use graph represents interactions between software elements.
    The use graph is directed; a node represents a method or a field.
    If a method 'a' calls a method 'b', there's exists an edge between the a and b.
    Also, there is an edge between a method node and a field node if this field is used in the method.
    """

    def __init__(self, id, path_file, debug_mode = False):
        #id of the use graph
        self.id = id
        #path of the GraphML file
        self.path_file = path_file
        #networkX graph
        self.graph = self.readFile()
        #all tests of use graph id -> name
        self.all_tests_id = {}
        #all tests of use graph name -> id
        self.all_tests_name = {}
        #all nodes of the use graph id -> name
        self.all_nodes_id = {}
        #all nodes of the use graph name -> id
        self.all_nodes_name = {}
        #all edges of the use graph
        self.all_edges = {}
        #number of tests
        self.number_of_tests = 0
        #number of edges
        self.number_of_edges = 0
        #number of nodes
        self.number_of_nodes = 0
        #liaisons test_id -> nodes impacted
        self.liaisons = {}
        #debugging mode
        self.debug_mode = debug_mode

    def __del__(self):
        print("Destruction of the use graph {0}".format(self.id))

    def readFile(self):
        """
        Abstract: Method to read the GraphML file and save the NetworkX graph matching
        """

        try:
            return nx.read_graphml(self.path_file)
        except Exception as excpt:
            raise excpt

    def run(self):
        """
        Abstract: Method to compute tests, nodes and edges
        """

        if self.debug_mode:
            begin_comp_tests_nodes = time.time()
        self.computeTestsAndNodes()
        if self.debug_mode:
            end_comp_tests_nodes = time.time()

        if self.debug_mode:
            begin_comp_edges = time.time()
        self.computeEdges()
        if self.debug_mode:
            end_comp_edges = time.time()

        if self.debug_mode:
            time_comp_tests_nodes = end_comp_tests_nodes - begin_comp_tests_nodes
            time_comp_edges = end_comp_edges - begin_comp_edges
            total_time = time_comp_tests_nodes + time_comp_edges
            print("Time for compute tests and nodes: {0} seconds".format(time_comp_tests_nodes))
            print("Time for compute edges: {0} seconds".format(time_comp_edges))
            print("Total time: {0} seconds".format(total_time))

    def computeTestsAndNodes(self):
        """
        Abstract: Method to compute and store all tests name
        """

        #to store test id
        i = 0

        #to store node id
        j = 0

        #for all nodes...
        for node in self.graph.nodes(data=True):

            #type abbreviation of the node - default 'V' (Variable)
            type_abbr = "v"

            #for Tests

            #store name and type of the node
            node_name, node_type = node
            #splitting
            if node_type['type'] == "VARIABLE":
                name_test = node_name.split("#")[0]
            else:
                name_test = node_name.split("(")[0]
                #change 'V' to 'M'
                type_abbr = "m"
            #if the test is not repertoried, we store it with an id
            if not name_test in self.all_tests_name:
                test_id = "t{0}".format(i)
                self.all_tests_name[name_test] = test_id
                self.all_tests_id[test_id] = name_test
                i = i + 1

            #for Nodes

            #get the node id
            node_id = "{0}-{1}{2}".format(self.all_tests_name[name_test], type_abbr, j)

            #store name -> id for node
            self.all_nodes_name[node_name] = node_id
            #store id -> name for node
            self.all_nodes_id[node_id] = node_name

            j = j + 1

        #number of tests is the number of test nodes stored
        self.number_of_tests = i

        #compute number of nodes
        self.number_of_nodes = self.graph.number_of_nodes()

    def computeEdges(self):
        """
        Abstract: Method to compute and store all edges (and the sum of theses edges) of the use graph
        """

        #id_edge : (id_first_node, id_second_node)
        for edge in self.graph.edges(data=True):
            #decomposition of the tuple
            source_edge, target_edge, data_edge = edge
            #we keep the id of the edge (by data_edge)
            self.all_edges[data_edge['id']] = (self.all_nodes_name[source_edge], self.all_nodes_name[target_edge])

        #compute number of edges
        self.number_of_edges = self.graph.number_of_edges()

    def computeLiaisons(self, mutation_node, impacted_nodes):
        """
        Abstract: Method to add some liaisons between tests and variables/methods
        """

        #get the id
        mutation_node_id = self.all_nodes_name[mutation_node]

        if self.debug_mode:
            print("Mutation {0}".format(mutation_node_id))

        #{mutation_node_id1: [node1_id, node2_id, ...], mutation_node_id2: [node1_id, node2_id, ...]}

        #if key does not exists, we create it
        if not mutation_node_id in self.liaisons:
            self.liaisons[mutation_node_id] = []
        #store all impacted nodes...
        for impacted_node in impacted_nodes:
            #store impacted node id in the 'mutation_node_id' array
            try:
                self.liaisons[mutation_node_id].append(self.all_nodes_name[impacted_node])
            except Exception as excpt:
                print("\tError for {0}: no id found for {1}!".format(mutation_node_id, excpt))

    def printInfo(self):
        """
        Abstract: Method to print (output standard) some informations about the use graph
        """

        return "Use graph {0} : {1} nodes and {2} edges / {3} tests".format(self.id, self.number_of_nodes, self.number_of_edges, self.number_of_tests)

    def visualize(self):
        """
        Abstract: Method to visualize the graph, with networkx tools and graphviz
        """

        nx.draw(self.graph)
        file_name = os.path.splitext(self.path_file)[0]
        plt.savefig("{0}.png".format(file_name))
