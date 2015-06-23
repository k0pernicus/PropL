import os
import time

import networkx as nx

from libs.xml_parsing_lib import parse_smf_run
from libs.xml_parsing_lib import parse_mutations
from libs.xml_parsing_lib import join_mutant_and_impacted_tests

from libs.learning_lib import dichotomicOnlineOptimization

from threading import Thread

not_authorized_files = ['.DS_Store', '__init__.py']

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
        #all cases from tests id -> name
        self.all_cases_id = {}
        #all cases from tests name -> id
        self.all_cases_name = {}
        #all nodes of the use graph id -> name
        self.all_nodes_id = {}
        #all nodes of the use graph name -> id
        self.all_nodes_name = {}
        #all edges of the use graph id -> name
        self.all_edges_id = {}
        #all edges of the use graph name -> id
        self.all_edges_name = {}
        #all edges used to propagate a bug
        self.usefull_edges = []
        #number of tests
        self.number_of_tests = 0
        #number of edges
        self.number_of_edges = 0
        #number of nodes
        self.number_of_nodes = 0
        #number of variables in nodes
        self.number_of_variables = 0
        #number of methods in nodes
        self.number_of_methods = 0
        #list of available mutants file
        self.available_mutants = []
        #liaisons mutant parents -> mutants child
        self.hash_mutants = {}
        #liaisons test_id -> nodes impacted
        self.mutants = {}
        #debugging mode
        self.debug_mode = debug_mode

    def __del__(self):
        print("Destruction of the use graph {0}".format(self.id))

    def readFile(self):
        """
        Abstract: Method to read the GraphML file and save the NetworkX graph matching
        """

        usegraph_name_file = "usegraph.graphml"

        try:
            return nx.read_graphml("{0}/{1}".format(self.path_file, usegraph_name_file))
        except Exception as excpt:
            raise excpt

    def run(self):
        """
        Abstract: Method to compute tests, nodes, edges and probabilities for each edge
        Debugging mode is usefull to know time costs
        """

        if self.debug_mode:
            begin_comp_tests = time.time()
        self.computeTests()
        if self.debug_mode:
            end_comp_tests = time.time()

        if self.debug_mode:
            begin_comp_nodes = time.time()
        self.computeNodes()
        if self.debug_mode:
            end_comp_nodes = time.time()

        if self.debug_mode:
            begin_comp_edges = time.time()
        self.computeEdges()
        if self.debug_mode:
            end_comp_edges = time.time()

        if self.debug_mode:
            begin_comp_mutants = time.time()
        self.computeMutants()
        if self.debug_mode:
            end_comp_mutants = time.time()

        if self.debug_mode:
            time_comp_tests = end_comp_tests - begin_comp_tests
            time_comp_nodes = end_comp_nodes - begin_comp_nodes
            time_comp_edges = end_comp_edges - begin_comp_edges
            time_comp_mutants = end_comp_mutants - begin_comp_mutants
            total_time = time_comp_tests + time_comp_nodes + time_comp_edges + time_comp_mutants
            print("Time to compute tests: {0} seconds".format(time_comp_tests))
            print("Time to compute nodes: {0} seconds".format(time_comp_nodes))
            print("Time to compute edges: {0} seconds".format(time_comp_edges))
            print("Time to compute mutants: {0} seconds".format(time_comp_mutants))
            print("Total time: {0} seconds".format(total_time))

    def computeTests(self):
        """
        Abstract: Method to compute tests from the smf.run.xml file
        """

        smf_name_file = "smf.run.xml"

        self.all_tests_id, self.all_tests_name, self.all_cases_id, self.all_cases_name = parse_smf_run("{0}/{1}".format(self.path_file, smf_name_file), self.debug_mode)

    def computeNodes(self):
        """
        Abstract: Method to compute and store all tests and nodes
        """

        variables_nb = 0

        methods_nb = 0

        j = 0

        #type attribute for the node type
        type_abbr = "m"

        name_test = ""

        #for all nodes...
        for node in self.graph.nodes(data = True):

            case_id = None

            #store name and type of the node
            node_name, node_type = node

            #for Nodes
            if node_type == "VARIABLE":
                type_abbr = "v"
                name_test = node_name.split("#")[0]
                j = variables_nb
                variables_nb = variables_nb + 1
            else:
                type_abbr = "m"
                name_test = node_name.split('(')[0]
                j = methods_nb
                methods_nb = methods_nb + 1

            #get the node id
            #if it's a test, get the id of the test...
            if name_test in self.all_cases_name:
                case_id = self.all_cases_name[name_test]['id']
                node_id = "{0}-{1}{2}".format(case_id, type_abbr, j)
            #else, put a 'no test' label (nt)
            else:
                node_id = "nt-{0}{1}".format(type_abbr, j)

            #store name -> id for node
            self.all_nodes_name[node_name] = node_id
            #store id -> name for node
            self.all_nodes_id[node_id] = node_name

            #store the good node (without 'nt') in cases_id dictionary
            if not case_id == None:
                self.all_cases_id[case_id]['nodes'].append(node_id)

        #compute number of nodes
        self.number_of_nodes = self.graph.number_of_nodes()

        #store number of variables in the use graph
        self.number_of_variables = variables_nb

        #store number of methods in the use graph
        self.number_of_methods = methods_nb

    def computeEdges(self):
        """
        Abstract: Method to compute and store all edges (and the sum of theses edges - weight) of the use graph
        Each edge is compute like : (source, target) -> id ; id -> source, target, weight
        """

        #id_edge : (id_first_node, id_second_node)
        for edge in self.graph.edges(data = True):
            #decomposition of the tuple
            source_edge, target_edge, data_edge = edge
            #we keep the id of the edge (by data_edge)
            self.all_edges_id[data_edge['id']] = {"source" : self.all_nodes_name[source_edge], "target" : self.all_nodes_name[target_edge], "weight": 0.5}
            #we keep the source (a, b) of the edge
            self.all_edges_name[(self.all_nodes_name[source_edge], self.all_nodes_name[target_edge])] = {"id" : data_edge['id']}

        #compute number of edges
        self.number_of_edges = self.graph.number_of_edges()

    def computeMutants(self):
        """
        Abstract: Method to compute and store mutants, and relations between them and nodes
        Please to see parse_mutations in xml_lib
        """

        #name directory of root mutants files
        root_directory_name = "AOR"

        #name directory of mutants files
        mutants_directory_name = "mutants"

        #root of mutations file
        mutations_name_file = "mutations.xml"

        base_dir = "{0}/{1}".format(self.path_file, root_directory_name)

        #parse mutants in the mutations_name_file
        self.hash_mutants, self.mutants = parse_mutations("{0}/{1}".format(base_dir, mutations_name_file), self.debug_mode)

        base_dir = "{0}/{1}".format(base_dir, mutants_directory_name)

        #for each mutant...
        for mutant_file in os.listdir(base_dir):
            if not mutant_file in not_authorized_files:
                #join their id to the id of failing tests
                join_mutant_and_impacted_tests("{0}/{1}".format(base_dir, mutant_file), self.mutants, self.all_cases_name, self.available_mutants, self.debug_mode)

    def transform_edge_name_as_edge_id(self, edge):
        """
        Abstract: Method to transform an edge composed by methods/fields name as an edge composed by the id of those methods/fields
        """

        return (self.all_nodes_name[edge[0]], self.all_nodes_name[edge[1]])

    def printInfo(self):
        """
        Abstract: Method to print (output standard) some informations about the use graph
        Return a string which contains these informations
        """

        return "Use graph {0} : {1} nodes ({4} variables - {5} methods) and {2} edges / {3} tests".format(self.id, self.number_of_nodes, self.number_of_edges, self.number_of_tests, self.number_of_variables, self.number_of_variables)

    def visualize(self):
        """
        Abstract: Method to visualize usefull edges
        """

        simple_visualization = nx.DiGraph()

        usefull_nodes = []

        usefull_edges = []

        for e in self.usefull_edges:

            source = self.all_edges_id[e]['source']

            target = self.all_edges_id[e]['target']

            if not source in usefull_nodes:

                usefull_nodes.append(source)

            if not target in usefull_nodes:

                usefull_nodes.append(target)

            if not (source, target) in usefull_edges:

                usefull_edges.append((source, target))

        simple_visualization.add_nodes_from(usefull_nodes)

        simple_visualization.add_edges_from(usefull_edges)

        graph_path = "{0}{1}.graphml".format(self.path_file, self.id)

        nx.write_graphml(simple_visualization, graph_path)

        os.system("python2.7 libs/graph_visualization.py {0} {1}".format(graph_path, self.id))
