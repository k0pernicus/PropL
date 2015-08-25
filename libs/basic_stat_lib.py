#Python3.4 - Antonin Carette

def computePrecision(true_positive, false_positive):
    """
    Abstract: Simple function to compute the precision of some examples
    true_positive: The number of true positive samples
    false_positive: The number of false positive samples
    """

    #if true_positive and false_positive are null, we admit 1
    if (true_positive + false_positive) == 0:
        return 1
    #else...
    return (true_positive) / (true_positive + false_positive)

def computeRecall(true_positive, false_negative):
    """
    Abstract: Simple function to compute the recall of some examples
    true_positive: The number of true positive samples
    false_negative: The number of false negative samples
    """

    #if true_positive and false_negative are null, we admit 1
    if (true_positive + false_negative) == 0:
        return 1
    return (true_positive) / (true_positive + false_negative)

def computeFScore(precision, recall):
    """
    Abstract: Simple function to compute the FScore of some examples
    precision: The precision of examples
    recall: The recall of examples
    """

    #if precision and recall are null, we admit 0
    if (precision + recall) == 0:
        return 0
    return 2 * ((precision * recall) / (precision + recall))

def computeAverage(list):
    """
    Abstract: Simple function to compute the average of elements in the list
    list: A list of integer of float elements
    """

    len_list = len(list)

    #if the list is empty, return 0
    if len_list == 0:
        return 0
    
    #else, compute the average score
    sum_elements = 0
    for element in list:
        sum_elements += element
    return sum_elements / len_list
