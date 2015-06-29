def chunksList(list, n):
    """
    Yield successive n-sized chunks from list
    """
    list_to_return = []
    for i in range(0, len(list), n):
        list_to_return += [list[i:i+n]]
    return list_to_return
