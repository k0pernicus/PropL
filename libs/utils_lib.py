def chunksList(list, n):
    """
    Yield successive n-sized chunks from list
    """
    list_to_return = []
    for i in range(0, len(list), n):
        list_to_return += [list[i:i+n]]
    return list_to_return

def getSomeInfos(usegraph):
    """
    Abstract: Method to get some stats on a UseGraph object (usegraph)
    """

    print("{0}{1}{0}".format("#"*20, usegraph.id))
    for edge_id in usegraph.usefull_edges:
        source = usegraph.all_edges_id[edge_id]['source']
        target = usegraph.all_edges_id[edge_id]['target']
        weight = usegraph.all_weights[usegraph.all_nodes_position_in_weights_matrix[source]][usegraph.all_nodes_position_in_weights_matrix[target]]
        print("## {0} ({1} -- {2}) : {3}".format(edge_id, source, target, weight))
    print("{0}".format("#"*(40 + len(usegraph.id))))
