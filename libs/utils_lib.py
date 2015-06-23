def chunks(list, n):
    """
    Yield successive n-sized chunks from l
    """
    for i in range(0, len(list), n):
        yield list[i:i+n]
