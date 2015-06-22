#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(path):

    graph = nx.read_graphml(path)

    nx.draw_networkx(graph)
    
    plt.show()

if __name__ == "__main__":

    path = sys.argv[1]

    print path

    draw_graph(path)
