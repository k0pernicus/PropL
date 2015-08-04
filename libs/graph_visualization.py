#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Python2 - Antonin Carette

import sys

import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(path, func):
    """
    Primitive to build a graph with networkx, and plot it with matplotlib
    Works ONLY with python 2.7
    path: The pathname of the graphml file
    func: The behavior to have in this function : show or/and save
    """

    #read the graphml
    graph = nx.read_graphml(path)

    #draw the graph with networkx
    nx.draw_networkx(graph)

    #"save" behavior
    if 'save' in func:
        plt.savefig("{0}.png".format(path.split('.graphml')[0]))
    #"show" behavior
    if 'show' in func:
        plt.show()

if __name__ == "__main__":
    """
    Script to visualize a graphml file (path as parameter)
    Works ONLY with python 2.7
    Arg 1: path of the graphml to visualize
    Arg 2: The id of the usegraph (to visualize)
    """

    version = sys.version()

    if not '2.7' in version:
        print("Please to install & run this script with Python2.7")
        sys.exit()

    #Get path of the graphml file
    path = sys.argv[1]

    #Get id of the usegraph to draw
    usegraph_id = sys.argv[2]

    func = ""

    #Ask the user if he wants to show or save the usegraph
    while (not 'show' in func) and (not 'save' in func):
        func = raw_input("Would you visualize ('show') or save ('save') the graph {0}? ".format(usegraph_id))

    #Draw the graph
    draw_graph(path, func)
