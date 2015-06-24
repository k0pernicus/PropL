def getSomeStats(usegraph):
    """
    Abstract: Method to get some stats on a UseGraph object (usegraph)
    """

    print("{0}{1}{0}".format("#"*20, usegraph.id))
    for edge_id in usegraph.usefull_edges:
        source = usegraph.all_edges_id[edge_id]['source']
        target = usegraph.all_edges_id[edge_id]['target']
        weight = usegraph.all_weights[usegraph.all_nodes_position_in_weights_matrix[source]][usegraph.all_nodes_position_in_weights_matrix[target]]
        print("{0} ({1} -- {2}) : {3}".format(edge_id, source, target, weight))
    print("{0}".format("#"*(40 + len(usegraph.id))))

def computePrecision(true_positive, false_positive):
    """
    Abstract: Simple function to compute the precision of some examples
    """

    return (true_positive) / (true_positive + false_positive)

def computeRecall(true_positive, false_negative):
    """
    Abstract: Simple function to compute the recall of some examples
    """

    return (true_positive) / (true_positive + false_negative)

def computeTrueNegativeRate(true_negative, false_positive):
    """
    Abstract: Simple function to compute the 'True negative rate' of some examples
    """

    return (true_negative) / (true_negative + false_positive)

def computeAccuracy(true_positive, true_negative, false_positive, false_negative):
    """
    Abstract: Simple function to compute the accuracy of some examples
    """

    return (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)
