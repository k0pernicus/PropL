import networkx as nx
import xml.etree.ElementTree as ET

import os
import sys

from xml.dom import minidom
from xml.sax import make_parser
from xml.sax.handler import ContentHandler

from libs.basic_stat_lib import computePrecision
from libs.basic_stat_lib import computeRecall
from libs.basic_stat_lib import computeFScore

nb_of_tests = 10

mutations_dir = "mutations/"

mutants_dir = "mutants/"

mutation_file = "mutations.xml"

smf_file = "smf.run.xml"

not_authorized_files = ['.DS_Store', '__init__.py']

def loadUseGraph(path):

    base_dir = os.listdir(path)

    list_of_usegraphs = []

    for usegraph in base_dir:
        if not usegraph in not_authorized_files and 'usegraph' in usegraph:
            list_of_usegraphs.append("{0}{1}".format(path, usegraph))

    return list_of_usegraphs

def loadMutationDir(path):

    base_dir = os.listdir(path)

    list_of_mutations_dir = []

    for dir in base_dir:
        if not dir in not_authorized_files:
            list_of_mutations_dir.append("{0}{1}/".format(path, dir))

    return list_of_mutations_dir

def loadMutantsFiles(path):

    base_dir = os.listdir(path)

    list_of_mutants_files = []

    for mutant in base_dir:
        if not mutant in not_authorized_files:
            list_of_mutants_files.append("{0}{1}".format(path, mutant))

    return list_of_mutants_files

def returnMutationsNodes(mutant_file):

    list_of_mutations = []

    tree = ET.parse(mutant_file)
    root = tree.getroot()

    mutant_id = root.get('id')

    for failing_tests in root.findall("failing"):

        for case_failing_test in failing_tests:

            list_of_mutations.append("{0}()".format(case_failing_test.text))

    for hanging_tests in root.findall("hanging"):

        for case_hanging_test in hanging_tests:

            list_of_mutations.append("{0}()".format(case_hanging_test.text))

    return mutant_id, list_of_mutations

def parseMutationFile(mutation_file):

    tree = ET.parse(mutation_file)
    root = tree.getroot()

    mutant_id_to_node_name = {}
    node_name_to_targets = {}

    for mutants_list in root.findall("mutants"):

        for mutant in mutants_list:

            if mutant.get('viable'):
                mutant_name = mutant.get('in')
                mutant_id = mutant.get('id')

                if not mutant_id in mutant_id_to_node_name:
                    mutant_id_to_node_name[mutant_id] = mutant_name
                else:
                    print("ERROR : duplicate data {0} -> {1}".format(mutant_id, mutant_name))

                if not mutant_name in node_name_to_targets:
                    node_name_to_targets[mutant_name] = []

    return mutant_id_to_node_name, node_name_to_targets

def parseSmfFile(path):

    tree = ET.parse("{0}{1}".format(path, smf_file))
    root = tree.getroot()

    smf_content = []

    for tests in root.findall("tests"):

        for cases in tests.findall("cases"):

            for case in cases.findall("case"):

                smf_content.append("{0}()".format(case.text))

    return smf_content

def computeTargetsFrom(node_name, edges, smf_content):

    #pile de noeuds (permettant de sauver tous les noeuds sur lesquels on passe)
    nodes_stack = []

    #liste de noeuds sur lesquels on est déjà passé
    list_of_nodes = []

    #liste des cibles
    targets_list = []

    #liste des tests
    tests_list = []

    #on ajoute d'ores-et-déjà le noeud muté...
    nodes_stack.append(node_name)
    list_of_nodes.append(node_name)

    #tant que la pile est pleine
    while len(nodes_stack) != 0:

        #le noeud actuel (celui étudié) est 'popé' de la liste
        actual_node = nodes_stack.pop()

        #on l'ajoute à la liste de noeud sur lequel on est passé
        list_of_nodes.append(actual_node)

        #actual_list correspond à l'ensemble des noeuds déjà passé
        actual_list = []

        #pour chaque arête
        for edge in edges:

            #on décompose l'arête avec source, cible
            source_edge, target_edge = edge

            #si la cible est le noeud actuel, on sauve la source de l'arête
            if target_edge == actual_node:
                actual_list.append(source_edge)

        #on ajoute à la liste des cibles le noeud étudié
        targets_list.append(actual_node)

        #on ajoute SEULEMENT les noeuds non-dupliqués dans la pile de noeuds
        for source in actual_list:
            if not source in list_of_nodes:
                nodes_stack.append(source)

    #on ajoute à la liste à retourner les noeuds intéressants, c'est-à-dire les noeuds de tests (contenus dans smf_content)
    for target in targets_list:
        if target in smf_content:
            tests_list.append(target)
        # else:
        #     print("{0} not append...".format(target))

    return tests_list

def doSomeStats(dict_exp, mutant_id_to_node_name, node_name_to_targets):

    #initialisation d'une liste contenant toutes les précisions calculées
    list_precision = []

    #initialisation d'une liste contenant toutes les valeurs de recall calculées
    list_recall = []

    #initialisation d'une liste contenant toutes les valeurs de fscore calculées
    list_fscore = []

    #pour chaque mutant issu des fichiers mutant_xxx.xml
    for mutant_id in dict_exp:

        #targets_algo contiendra toutes les cibles issues de l'algo du mutant mutant_id
        targets_algo = node_name_to_targets[mutant_id_to_node_name[mutant_id]]

        #targets_exp contiendra toutes les cibles expérimentales du mutant mutant_id
        targets_exp = dict_exp[mutant_id]

        #initialisation des variables à 0
        true_positive = 0

        false_positive = 0

        false_negative = 0

        #si les deux listes ne sont pas vides, alors on étudie le nombre de vrai positifs
        if len(targets_exp) != 0 and len(targets_algo) !=0:

            #pour chaque cible expérimentale...
            for target_exp in targets_exp:

                #drapeau à Faux
                visited = False

                #pour chaque cible de l'algo...
                for target_algo in targets_algo:

                    #si la cible expérimentale est la même que celle de l'algo ET qu'elle n'a pas été visité...
                    if target_exp == target_algo and not visited:

                        #on augmente le nombre de vrai positifs
                        true_positive += 1

                        #changement du booléen à True
                        visited = True

        #Les faux positifs sont comptés d'après le reste des cibles issus de l'algo
        false_positive = len(targets_algo) - true_positive

        #Les faux négatifs sont comptés d'après le reste des cibles issus de l'expérience
        false_negative = len(targets_exp) - true_positive

        precision_comp = computePrecision(true_positive, false_positive)

        recall_comp = computeRecall(true_positive, false_negative)

        fscore_comp = computeFScore(precision_comp, recall_comp)

        #On ajoute dans la liste de précisions la précision qui va être calculé selon les valeurs données
        list_precision.append(precision_comp)

        #de même pour le recall
        list_recall.append(recall_comp)

        list_fscore.append(fscore_comp)

    #Tri des listes
    list_precision.sort()

    list_recall.sort()

    list_fscore.sort()

    #On renverra la médiane de précision / recall
    median_list_precision = round(len(list_precision) / 2)

    median_list_recall = round(len(list_recall) / 2)

    median_list_fscore = round(len(list_fscore) / 2)

    return list_precision[median_list_precision], list_recall[median_list_recall], list_fscore[median_list_fscore]

if __name__ == "__main__":
    """
        Program to verify the results from Vincenzo Musco in his thesis.
    """
    path = sys.argv[1]

    if '--debug' in sys.argv:
        debug_mode = True
    else:
        debug_mode = False

    #récupération de la liste des usegraphs
    list_of_usegraphs = loadUseGraph(path)

    #récupération de la liste des répertoires contenant les mutations
    list_of_mutations_dir = loadMutationDir("{0}{1}".format(path, mutations_dir))

    if debug_mode:
        print("usegraphs : {0}".format(list_of_usegraphs))
        print("mutations dir : {0}".format(list_of_mutations_dir))

    #pour chaque fichier usegraph
    for usegraph in list_of_usegraphs:

        #on 'sauve' celui qui nous intéresse
        graphml = nx.read_graphml(usegraph)

        #on parse le contenu du fichier smf.run.xml associé
        smf_content = parseSmfFile(path)

        #pour chaque dossier contenant les mutations (ABS, AOR, LCR, ROR, ...)
        for mutation_dir in list_of_mutations_dir:

            #on récupère une table de hachage permettant de récupérer le nom du mutant en fonction de son id (mutant_id_to_node_name), et une table de hachage contenant la liste des tests impactés en fonction des noms des mutants
            mutant_id_to_node_name, node_name_to_targets = parseMutationFile("{0}{1}".format(mutation_dir, mutation_file))

            #la liste des fichiers mutants est sauvée
            list_of_mutants_files = loadMutantsFiles("{0}{1}".format(mutation_dir, mutants_dir))

            #une table contenant les résultats expérimentaux (id_mutant -> tests_impactés) est créée
            dict_exp = {}

            #pour chaque fichier mutant
            for mutant_file in list_of_mutants_files:

                #on sauve son id et la liste des impacts
                mutant_id, list_of_mutations = returnMutationsNodes(mutant_file)

                dict_exp[mutant_id] = list_of_mutations

            #pour chaque mutant intéressant, sauvé dans dict_exp
            for interesting_mutant_id in dict_exp:

                #on sauve la liste des impacts obtenu par un algo (computeTargetsFrom), dans node_name_to_targets
                node_name = mutant_id_to_node_name[interesting_mutant_id]

                node_name_to_targets[node_name] = computeTargetsFrom(node_name, graphml.edges(), smf_content)

            #on récupère la médiane précision/recall  et on l'affiche
            precision_median, recall_median, fscore_median = doSomeStats(dict_exp, mutant_id_to_node_name, node_name_to_targets)

            print("usegraph {0} with dir {1} : {2} / {3} -> {4}".format(usegraph, mutation_dir, precision_median, recall_median, fscore_median))
