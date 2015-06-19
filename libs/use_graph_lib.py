import os
import time

import networkx as nx
import matplotlib.pyplot as plt

from libs.xml_lib import parse_smf_run
from libs.xml_lib import parse_mutations
from libs.xml_lib import join_mutant_and_impacted_tests

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
        #all edges of the use graph
        self.all_edges = {}
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
        Abstract: Method to compute tests, nodes and edges
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
            print("Time compute nodes: {0} seconds".format(time_comp_nodes))
            print("Time compute edges: {0} seconds".format(time_comp_edges))
            print("Time compute mutants: {0} seconds".format(time_comp_mutants))
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
                node_id = "{0}-{1}{2}".format(self.all_cases_name[name_test]['id'], type_abbr, j)
            #else, put a 'no test' label (nt)
            else:
                node_id = "nt-{0}{1}".format(type_abbr, j)

            #store name -> id for node
            self.all_nodes_name[node_name] = node_id
            #store id -> name for node
            self.all_nodes_id[node_id] = node_name

        #compute number of nodes
        self.number_of_nodes = self.graph.number_of_nodes()

        #store number of variables in the use graph
        self.number_of_variables = variables_nb

        #store number of methods in the use graph
        self.number_of_methods = methods_nb

    def computeEdges(self):
        """
        Abstract: Method to compute and store all edges (and the sum of theses edges) of the use graph
        """

        #id_edge : (id_first_node, id_second_node)
        for edge in self.graph.edges(data = True):
            #decomposition of the tuple
            source_edge, target_edge, data_edge = edge
            #we keep the id of the edge (by data_edge)
            self.all_edges[data_edge['id']] = {"source" : self.all_nodes_name[source_edge], "target" : self.all_nodes_name[target_edge], "weight": 0.5}

        #compute number of edges
        self.number_of_edges = self.graph.number_of_edges()

    def computeMutants(self):
        """
        Abstract: Method to compute and store mutants and relations between them and nodes
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
            #join their id to the id of failing tests
            join_mutant_and_impacted_tests("{0}/{1}".format(base_dir, mutant_file), self.mutants, self.all_cases_name, self.available_mutants, self.debug_mode)

    def getSimpleRepresentationForMutants(self):
        """
        Abstract: Method to return a representation of which mutant is the child of a father mutant
        """

        simple_representation_for_mutants = {}

        #each mutant parent contains a list of mutants
        for mutant in self.hash_mutants:

            simple_representation_by_mutant = {}

            #searching for all mutant id in the list of mutants
            for single_mutant_id in self.hash_mutants[mutant]['list_mutants']:

                #this field is a tag to know if there's multiple tests for the same mutation
                position_of_the_mutation = "{0}||{1}".format(self.mutants[single_mutant_id]['from'], self.mutants[single_mutant_id]['to'])

                if not position_of_the_mutation in simple_representation_by_mutant:
                    simple_representation_by_mutant[position_of_the_mutation] = []

                simple_representation_by_mutant[position_of_the_mutation].append(single_mutant_id)

            #we have now the representation of all mutants children for a parent
            simple_representation_for_mutants[mutant] = simple_representation_by_mutant

        return simple_representation_for_mutants

    def getComplexRepresentationForMutants(self):
        """
        Abstract: Method to return a complex representation for mutants : for a mutant father, which mutant (and how much) has been failed for a mutant child
        """

        simple_representation_for_mutants = self.getSimpleRepresentationForMutants()

        complex_representation_for_mutants = {}

        #mutant : {position_of_the_mutation1 : [test1,...], position_of_the_mutation2 : [test1,...]}
        for mutant_list in simple_representation_for_mutants:

            #number of mutants in the hash map is the number of tests
            nb_of_tests = len(self.hash_mutants[mutant_list]['list_mutants'])

            all_tests = {}

            for mutant in simple_representation_for_mutants[mutant_list]:

                #mutants_id is a list which represents id of each mutant
                mutants_id = simple_representation_for_mutants[mutant_list][mutant]

                if self.debug_mode:
                    print("mutant {0}".format(mutant))

                #for each mutant id...
                for mutant_id in mutants_id:

                    #decrement the nb of tests if the mutant is not in a file test!
                    if not mutant_id in self.available_mutants:

                        if self.debug_mode:
                            print("mutant_id {0} not in the list...".format(mutant_id))

                        nb_of_tests = nb_of_tests - 1

                    else:
                        if self.debug_mode:
                            print("mutant_id {0} in the list...".format(mutant_id))

                        #store the list of impacted tests
                        impacted_tests = self.mutants[mutant_id]['impacted_tests']

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
                            if self.debug_mode:
                                print("no impacted tests for {0}".format(mutant_id))

            #compute the average
            for test in all_tests:
                all_tests[test] = all_tests[test] / nb_of_tests

            #get only usefull representations (the value isn't null...)
            complex_representation_for_mutants[mutant_list] = all_tests

        complex_representation_for_mutants = dict((key, value) for key, value in complex_representation_for_mutants.items() if len(value) != 0)

        return complex_representation_for_mutants

    def computeProbabilities(self):
        """
        Abstract: Method to compute probabilities on edges
        """

        #TODO Ajouter les poids aux arêtes!!!!!

        print(self.getComplexRepresentationForMutants())

    def printInfo(self):
        """
        Abstract: Method to print (output standard) some informations about the use graph
        Return a string which contains these informations
        """

        return "Use graph {0} : {1} nodes ({4} variables - {5} methods) and {2} edges / {3} tests".format(self.id, self.number_of_nodes, self.number_of_edges, self.number_of_tests, self.variables_nb, self.methods_nb)

    def saveOnBoard(self):
        """
        Abstract: Method to save the visualization
        """

        nx.draw(self.graph)
        file_name = os.path.splitext(self.path_file)[0]
        plt.savefig("{0}.png".format(file_name))
