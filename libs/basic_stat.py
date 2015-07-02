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

    return (true_positive) / (true_positive + false_negative)
