prefix = "Rslts_propl/Rslts_propl_"
suffix = ".tex"

def initTexFile(file):

    path = "{0}{1}{2}".format(prefix, file, suffix)

    init_string = "\\documentclass[a4paper]{article}\n"
    init_string += "\\begin{document}\n"

    tex_file = open(path, "a")
    tex_file.write(init_string)
    tex_file.close()

def writeIntoTexFile(file, data):

    path = "{0}{1}{2}".format(prefix, file, suffix)

    len_data = len(data)

    info = "\\hline\n"
    for i in range(0, len_data - 1):
        info += "{0}&".format(data[i])
    info += "{0}\n".format(data[len_data - 1])
    info += "\\\\\n"

    tex_file = open(path, "a")
    tex_file.write(info)
    tex_file.close()

def beginTabular(file, nb_columns):

    path = "{0}{1}{2}".format(prefix, file, suffix)

    typo_columns = "{"
    typo_columns += ("|l"*nb_columns)
    typo_columns += "|}"

    tex_file = open(path, "a")
    tex_file.write("\\begin{tabular}"+typo_columns+"\n")
    tex_file.close()

def addDefaultTagsIntoTabular(file):

    path = "{0}{1}{2}".format(prefix, file, suffix)

    to_write = "\\hline\n"
    to_write += "Package&Algorithm&Usegraph&M.Operator&P&R&F\n"
    to_write += "\\\\\n"

    tex_file = open(path, "a")
    tex_file.write(to_write)
    tex_file.close()

def closeTabular(file):

    path = "{0}{1}{2}".format(prefix, file, suffix)

    tex_file = open(path, "a")
    tex_file.write("\\end{tabular}\n")
    tex_file.close()

def closeTexFile(file):

    path = "{0}{1}{2}".format(prefix, file, suffix)

    tex_file = open(path, "a")
    tex_file.write("\\end{document}\n")
    tex_file.close()

def cleanTexFile(file):

    path = "{0}{1}{2}".format(prefix, file, suffix)

    tex_file = open(path, "w")
    tex_file.truncate()
    tex_file.close()
