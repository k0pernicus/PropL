import os
import time
import random

import networkx as nx
import numpy as np

from libs.xml_parsing_lib import parseSmfRun
from libs.xml_parsing_lib import parseMutations
from libs.xml_parsing_lib import joinMutantAndImpactedTests
from libs.xml_parsing_lib import returnTheMutantNode

from libs.utils_lib import chunksList

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

    def __init__(self, id, path_file, debug_mode = False, number_split_tests = 10, propagation_mod_computing = 'all',propagation_mod_tests = 'all'):
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
        #all nodes position in the weights matrix
        self.all_nodes_position_in_weights_matrix = {}
        #all weights between two nodes
        self.all_weights = np.zeros(0)
        #represents the number of splits in the mutants file list
        self.number_split_tests = number_split_tests
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
        #list of files to learn
        self.files_to_learn = []
        #list of files for some tests
        self.files_for_tests = []
        #list of nodes to test
        self.nodes_for_tests = []
        #list of available mutants file
        self.available_mutants = []
        #liaisons mutant parents -> mutants child
        self.hash_mutants = {}
        #liaisons mutant parents -> mutants child FOR TESTS
        self.mutants = {}
        #debugging mode
        self.debug_mode = debug_mode
        #propagation mod to compute probabilities
        self.propagation_mod_computing = propagation_mod_computing
        #propagation mod to make tests
        self.propagation_mod_tests = propagation_mod_tests

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
            begin_comp_weights_matrix = time.time()
        self.initWeightsMatrix()
        if self.debug_mode:
            end_comp_weights_matrix = time.time()

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
            time_comp_weights_matrix = end_comp_weights_matrix - begin_comp_weights_matrix
            time_comp_edges = end_comp_edges - begin_comp_edges
            time_comp_mutants = end_comp_mutants - begin_comp_mutants
            total_time = time_comp_tests + time_comp_nodes + time_comp_weights_matrix + time_comp_edges + time_comp_mutants
            print("Time to compute tests: {0} seconds".format(time_comp_tests))
            print("Time to compute nodes: {0} seconds".format(time_comp_nodes))
            print("Time to init weights matrix: {0} seconds".format(time_comp_weights_matrix))
            print("Time to compute edges: {0} seconds".format(time_comp_edges))
            print("Time to compute mutants: {0} seconds".format(time_comp_mutants))
            print("Total time: {0} seconds".format(total_time))

    def computeTests(self):
        """
        Abstract: Method to compute tests from the smf.run.xml file
        """

        smf_name_file = "smf.run.xml"

        self.all_tests_id, self.all_tests_name, self.all_cases_id, self.all_cases_name = parseSmfRun("{0}/{1}".format(self.path_file, smf_name_file), self.debug_mode)

    def computeNodes(self):
        """
        Abstract: Method to compute and store all tests and nodes
        """

        variables_nb = 0

        methods_nb = 0

        j = 0

        position_in_matrix_weights = 0

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
            self.all_nodes_name[node_name] = {'id': node_id, 'sources': []}
            #store id -> name for node
            self.all_nodes_id[node_id] = node_name

            #store the good node (without 'nt') in cases_id dictionary
            if not case_id == None:
                self.all_cases_id[case_id]['nodes'].append(node_id)

            #store the position of the node id in the weights matrix
            self.all_nodes_position_in_weights_matrix[node_id] = position_in_matrix_weights

            position_in_matrix_weights += 1

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
            self.all_edges_id[data_edge['id']] = {"source" : self.all_nodes_name[source_edge]['id'], "target" : self.all_nodes_name[target_edge]['id']}
            #we store an arbitrary weight to the edge
            self.all_weights[self.all_nodes_position_in_weights_matrix[self.all_nodes_name[source_edge]['id']]][self.all_nodes_position_in_weights_matrix[self.all_nodes_name[target_edge]['id']]] = 0.5
            #we keep the source (a, b) of the edge
            self.all_edges_name[(self.all_nodes_name[source_edge]['id'], self.all_nodes_name[target_edge]['id'])] = {"id" : data_edge['id']}
            #store all target
            self.all_nodes_name[target_edge]['sources'].append(self.all_nodes_name[source_edge]['id'])

        #compute number of edges
        self.number_of_edges = self.graph.number_of_edges()

    def computeMutants(self):
        """
        Abstract: Method to compute and store mutants, and relations between them and nodes
        Please to see parseMutations in xml_lib
        """

        #name directory of root mutants files
        root_directory_name = "AOR"

        #name directory of mutants files
        mutants_directory_name = "mutants"

        #root of mutations file
        mutations_name_file = "mutations.xml"

        base_dir = "{0}/{1}".format(self.path_file, root_directory_name)

        #parse mutants in the mutations_name_file
        self.hash_mutants, self.mutants = parseMutations("{0}/{1}".format(base_dir, mutations_name_file), self.debug_mode)

        base_dir = "{0}/{1}".format(base_dir, mutants_directory_name)

        self.splitLearningAndTestingFiles(base_dir)

        #for each mutant...
        for mutant_file in self.files_to_learn:
            #join their id to the id of failing tests
            joinMutantAndImpactedTests("{0}/{1}".format(base_dir, mutant_file), self.mutants, self.all_cases_name, self.available_mutants, self.debug_mode)

        for mutant_file_test in self.files_for_tests:
            #store id of nodes available for tests
            mutant_node = returnTheMutantNode("{0}/{1}".format(base_dir, mutant_file_test))
            node_id = self.all_nodes_name[self.mutants[mutant_node]['name']]['id']
            if self.debug_mode:
                print("{0} -> {1} add as mutant test (file {2})...".format(self.id, self.mutants[mutant_node]['name'], mutant_file_test))
            self.nodes_for_tests.append(node_id)

    def initWeightsMatrix(self):
        """
        Abstract: Method to create and initialize the weights matrix
        """

        self.all_weights = np.zeros((self.number_of_nodes, self.number_of_nodes))

    def splitLearningAndTestingFiles(self, base_dir):
        """
        Abstract: Method to split mutant files for tests and to learn (like cross validation)
        """

        #save all files in the mutant directory
        mutants_filename_table = os.listdir(base_dir)

        #Remove all unauthorized files
        for file in mutants_filename_table:
            if file in not_authorized_files:
                mutants_filename_table.remove(file)

        number_of_mutants_file = len(mutants_filename_table)

        #split the list in number_split_tests
        mutants_filename_table_splitted = chunks_list(mutants_filename_table, self.number_split_tests)

        position_to_pop = random.randint(0, len(mutants_filename_table_splitted) - 1)

        if self.debug_mode:
            print("{0} -> Pop position {1} in list of {2} mutants".format(self.id, position_to_pop, len(mutants_filename_table_splitted)))

        #pop a random entry -> for tests
        self.files_for_tests = mutants_filename_table_splitted.pop(position_to_pop)

        #add other files into files_to_learn
        for mutant_filename in mutants_filename_table_splitted:
            self.files_to_learn += mutant_filename

        if self.debug_mode:
            print("{0} -> ({1} tests for {2} learning files) / {3}".format(self.id, len(self.files_for_tests), len(self.files_to_learn), number_of_mutants_file))
            print("files for tests: {0}".format(self.files_for_tests))

    def transform_edge_name_as_edge_id(self, edge):
        """
        Abstract: Method to transform an edge composed by methods/fields name as an edge composed by the id of those methods/fields
        """

        return (self.all_nodes_name[edge[0]]['id'], self.all_nodes_name[edge[1]]['id'])

    def printInfo(self):
        """
        Abstract: Method to print (output standard) some informations about the use graph
        Return a string which contains these informations
        """

        return "Use graph {0} : {1} nodes ({4} variables - {5} methods) and {2} edges / {3} tests".format(self.id, self.number_of_nodes, self.number_of_edges, self.number_of_tests, self.number_of_variables, self.number_of_methods)

    def visualize(self):
        """
        Abstract: Method to visualize usefull edges
        """

        simple_visualization = nx.DiGraph()
        usefull_nodes = []
        usefull_edges = []
        #visu_dir is a field to store the name of the directory which contains visualization files
        visu_dir = "visu"

        for e in self.usefull_edges:
            source = self.all_edges_id[e]['source']
            target = self.all_edges_id[e]['target']

            #store all usefull nodes (usefull nodes are nodes in the mutation graph)
            if not source in usefull_nodes:
                usefull_nodes.append(source)

            if not target in usefull_nodes:
                usefull_nodes.append(target)

            #store all usefull edges (usefull edges are edges in the mutation graph)
            if not (source, target) in usefull_edges:
                usefull_edges.append((source, target))

        simple_visualization.add_nodes_from(usefull_nodes)
        simple_visualization.add_edges_from(usefull_edges)

        #path to store the visualization (graphml)
        graph_path = "{0}{1}/{2}.graphml".format(self.path_file, visu_dir, self.id)

        nx.write_graphml(simple_visualization, graph_path)

        #call the script (with Python2.7) to visualize the graphml file, or to save it
        os.system("python2.7 libs/graph_visualization.py {0} {1}".format(graph_path, self.id))
