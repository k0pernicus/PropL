import csv

path = "results_antonin.csv"

def chunksList(list, n):
    """
    Yield successive n-sized chunks from list
    list: The list to chunks
    n: The number of elements in each sublist
    """
    list_to_return = []
    for i in range(0, len(list), n):
        list_to_return += [list[i:i+n]]
    return list_to_return

def getSomeInfos(usegraph):
    """
    Abstract: Method to get some informations for the usegraph given as parameter : weight for each edge in usefull_edges field
    usegraph: The usegraph to study to get some informations
    """

    print("{0}{1}{0}".format("#"*20, usegraph.id))
    for edge_id in usegraph.usefull_edges:
        source = usegraph.all_edges_id[edge_id]['source']
        target = usegraph.all_edges_id[edge_id]['target']
        weight = usegraph.all_weights[usegraph.all_nodes_position_in_weights_matrix[source]][usegraph.all_nodes_position_in_weights_matrix[target]]
        print("## {0} ({1} -- {2}) : {3}".format(edge_id, source, target, weight))
    print("{0}".format("#"*(40 + len(usegraph.id))))

def writeIntoCSVFile(data):
    """
    Abstract: Method to save into a CSV file results of tests
    data: Simple data to save, in a list
    """

    with open(path, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(data)

def cleanCSVFile():
    """
    Abstract: Method to clean the CSV file (no data inside)
    """

    csv_file = open(path, "w")
    csv_file.truncate()
    csv_file.close()
