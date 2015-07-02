def computePrecision(true_positive, false_positive):
    """
    Abstract: Simple function to compute the precision of some examples
    """

    if (true_positive + false_positive) == 0:
        return 1
    return (true_positive) / (true_positive + false_positive)

def computeRecall(true_positive, false_negative):
    """
    Abstract: Simple function to compute the recall of some examples
    """

    if (true_positive + false_negative) == 0:
        return 1
    return (true_positive) / (true_positive + false_negative)

def computeFScore(precision, recall):
    """
    Abstract: Simple function to compute the FScore of some examples
    """

    if (precision + recall) == 0:
        return 0
    return 2 * ((precision * recall) / (precision + recall))
