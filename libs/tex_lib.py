path = "results_antonin.tex"

def initTexFile():

    init_string = "\\documentclass[a4paper]{article}\n"
    init_string += "\\begin{document}\n"

    tex_file = open(path, "a")
    tex_file.write(init_string)
    tex_file.close()

def writeIntoTexFile(data):

    len_data = len(data)

    info = "\\hline\n"
    for i in range(0, len_data - 1):
        info += "{0}&".format(data[i])
    info += "{0}\n".format(data[len_data - 1])
    info += "\\\\\n"

    tex_file = open(path, "a")
    tex_file.write(info)
    tex_file.close()

def beginTabular(nb_columns):

    typo_columns = "{"
    typo_columns += ("|l"*nb_columns)
    typo_columns += "|}"

    tex_file = open(path, "a")
    tex_file.write("\\begin{tabular}"+typo_columns+"\n")
    tex_file.close()

def closeTabular():

    tex_file = open(path, "a")
    tex_file.write("\\end{tabular}\n")
    tex_file.close()

def closeTexFile():

    tex_file = open(path, "a")
    tex_file.write("\\end{document}\n")
    tex_file.close()

def cleanTexFile():

    tex_file = open(path, "w")
    tex_file.truncate()
    tex_file.close()
