def chunks_list(list, n):
    """
    Yield successive n-sized chunks from list
    """
    for i in range(0, len(list), n):
        yield list[i:i+n]
