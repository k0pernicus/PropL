import networkx as nx
import xml.etree.ElementTree as ET
import os
import sys

from xml.dom import minidom
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

mutations_dir = "mutations/"
mutants_dir = "mutants/"

mutations_file = "mutations.xml"

not_authorized_files = ['.DS_Store', '__init__.py', '__pycache__']

def parse_mutations_file(dir_content):

    id_mutant_to_name = {}

    name_mutant_to_id = {}

    try:
        tree = ET.parse(dir_content)
        root = tree.getroot()

        #for each mutant list in the mutations XML file
        for mutants_list in root.findall("mutants"):

            for mutant in mutants_list:

                #if mutant is viable...
                if mutant.get('viable'):
                    mutant_name = mutant.get('in')
                    if not mutant_name in name_mutant_to_id:
                        name_mutant_to_id[mutant_name] = []

                    #id to name
                    mutant_id = mutant.get('id')
                    id_mutant_to_name[mutant_id] = mutant_name

                    #name to id
                    name_mutant_to_id[mutant_name].append(mutant_id)

    except Exception as e:
        print("[parse_mutations_file] ERROR with file {0} : {1}".format(dir_content, e))

    return id_mutant_to_name, name_mutant_to_id

def parse_mutant_file(mutant_file):

    targets = []

    try:

        tree = ET.parse(mutant_file)
        root = tree.getroot()

        mutation_id = root.get('id')

        for failing_tests in root.findall("failing"):

            for case_failing_test in failing_tests:

                targets.append(case_failing_test.text)

        #hanging_tests

        for hanging_tests in root.findall("hanging"):

            for case_hanging_test in hanging_tests:

                targets.append(case_hanging_test.text)

        return mutation_id, targets

    except Exception as e:
        print("[parse_mutant_file] ERROR with file {0} : {1}".format(mutant_file, e))
        return None, targets

def compute_paths(project, usegraph):

    princ_dir = "{0}{1}".format(project, mutations_dir)

    id_mutant_to_name = {}
    name_mutant_to_id = {}

    paths = {}

    nb_paths = 0

    for mutator in os.listdir(princ_dir):
        if not mutator in not_authorized_files:

            if not mutator[-1] == "/":
                mutator += "/"
            mutator = princ_dir + mutator

            mutator_dir_content = mutator + "mutations.xml"
            id_mutant_to_name, name_mutant_to_id = parse_mutations_file(mutator_dir_content)

            mutator_dir_content = mutator + mutants_dir
            for mutant_file in os.listdir(mutator_dir_content):

                if not mutant_file in not_authorized_files:

                    mutant_file = mutator_dir_content + mutant_file

                    source_id, targets = parse_mutant_file(mutant_file)
                    if source_id:
                        source_name = id_mutant_to_name[source_id]
                        for target in targets:
                            try:
                                to_compute = False
                                if not source_name in paths:
                                    paths[source_name] = []
                                    to_compute = True
                                if not target in paths[source_name]:
                                    paths[source_name].append(target)
                                    to_compute = True
                                if to_compute:
                                    for p in nx.all_simple_paths(usegraph, target+'()',source_name):
                                        nb_paths += 1
                            except Exception as e:
                                pass
                                #print("[compute_paths] ERROR to compute path between {0} and {1} : {2}".format(source_name, target, e))

    return nb_paths

def main():
    project = sys.argv[1]

    if project[-1] != "/":
        project += "/"

    usegraphs = []

    #Get usefull graphs

    if "--usegraph" in sys.argv:
        usegraphs.append("{0}{1}".format(project, sys.argv[sys.argv.index("--usegraph") + 1]))
    else:
        for f in os.listdir(project):
            if "usegraph" in f:
                usegraphs.append("{0}{1}".format(project, f))

    for ug in usegraphs:
        print("READ {0}".format(ug))

        g = nx.read_graphml(ug)

        nb_nodes = g.number_of_nodes()
        nb_edges = g.number_of_edges()

        nb_paths = compute_paths(project, g)

        print("Stats for {0}:".format(ug))
        print("\tnumber of nodes : {0}".format(nb_nodes))
        print("\tnumber of edges : {0}".format(nb_edges))
        print("\tnumber of paths : {0}".format(nb_paths))

    print("Done!")

if __name__ == '__main__':
    main()
