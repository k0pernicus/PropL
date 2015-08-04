#Python3.4 - Antonin Carette

"""
prefix is the prefix of the path's tex file to save
"""
prefix = "Rslts_propl_"

"""
suffix is the extension of the tex file
"""
suffix = ".tex"

def initTexFile(rslts_dir, file):
    """
    Function to initialize the tex file
    file: The tex file
    """

    path = "{0}/{1}{2}{3}".format(rslts_dir, prefix, file, suffix)

    init_string = "\\documentclass[a4paper]{article}\n"
    init_string += "\\begin{document}\n"

    tex_file = open(path, "a")
    tex_file.write(init_string)
    tex_file.close()

def writeIntoTexFile(rslts_dir, file, data):
    """
    Function to write some data into the tex file
    file: The tex file
    data: The data to write into the tex file
    """

    path = "{0}/{1}{2}{3}".format(rslts_dir, prefix, file, suffix)

    len_data = len(data)

    info = "\\hline\n"
    for i in range(0, len_data - 1):
        info += "{0}&".format(data[i])
    info += "{0}\n".format(data[len_data - 1])
    info += "\\\\\n"

    tex_file = open(path, "a")
    tex_file.write(info)
    tex_file.close()

def beginTabular(rslts_dir, file, nb_columns):
    """
    Function to write some code to initialize a tabular (with a certain number of columns), into the tex file
    file: The tex file
    nb_columns: The number of columns to write
    """

    path = "{0}/{1}{2}{3}".format(rslts_dir, prefix, file, suffix)

    typo_columns = "{"
    typo_columns += ("|l"*nb_columns)
    typo_columns += "|}"

    tex_file = open(path, "a")
    tex_file.write("\\begin{tabular}"+typo_columns+"\n")
    tex_file.close()

def addDefaultTagsIntoTabular(rslts_dir, file):
    """
    Function to write default tags into the tabular of the tex file
    file: The tex file
    """

    path = "{0}/{1}{2}{3}".format(rslts_dir, prefix, file, suffix)

    to_write = "\\hline\n"
    to_write += "Package&Algorithm&Usegraph&#Batchs&M.Operator&P&R&F\n"
    to_write += "\\\\\n"

    tex_file = open(path, "a")
    tex_file.write(to_write)
    tex_file.close()

def closeTabular(rslts_dir, file):
    """
    Function to close the tabular in the tex file
    file: The tex file
    """

    path = "{0}/{1}{2}{3}".format(rslts_dir, prefix, file, suffix)

    tex_file = open(path, "a")
    tex_file.write("\\end{tabular}\n")
    tex_file.close()

def closeTexFile(rslts_dir, file):
    """
    Function to close the tex file
    file: The tex file
    """

    path = "{0}/{1}{2}{3}".format(rslts_dir, prefix, file, suffix)

    tex_file = open(path, "a")
    tex_file.write("\\end{document}\n")
    tex_file.close()

def cleanTexFile(rslts_dir, file):
    """
    Function to clean the tex file (no data & structures in this one)
    file: The tex file
    """

    path = "{0}/{1}{2}{3}".format(rslts_dir, prefix, file, suffix)

    tex_file = open(path, "w")
    tex_file.truncate()
    tex_file.close()
