#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(path):
    """
    Script to build a graph with networkx, and plot it with matplotlib
    ONLY with python 2.7
    """
    graph = nx.read_graphml(path)

    nx.draw_networkx(graph)

    plt.savefig("{0}.png".format(path.split('.graphml')[0]))

    plt.show()

if __name__ == "__main__":
    """
    Script to visualize a graphml file (path as parameter)
    ONLY with python 2.7
    """

    path = sys.argv[1]

    draw_graph(path)
