import sys

projects = ["commons-codec", "commons-collections", "commons-io", "commons-lang", "shindig", "sonar", "spojo"]
mutators = ["ABS", "AOR", "LCR", "ROR", "UOI"]
draw_styles = ["thick", "dotted", "dashed", "very thin", "thin, color=gray!40"]
default_value = -1
init = 1
gap = 3
limit = 30

#commons-codec&update_all_edges_online_opt&usegraph_C.graphml&1&AOR&0.79&0.65&0.69

def init_mutators_tab():
    mutators_tab = {}
    for m in mutators:
        mutators_tab[m] = {}
        for i in range(0, limit + 1, gap):
            if i == 0:
                i = init
            mutators_tab[m][i] = default_value
    return mutators_tab

def transform_mutators_tab_into_graph(mutators_tab):

    to_return = ""

    sorted_mutators = sorted(mutators_tab)

    for mutator in sorted_mutators:
        index_for_tab = mutators.index(mutator)
        to_return += "% {0}\n".format(mutator)
        to_return += "\draw[{0}]\n".format(draw_styles[index_for_tab])

        sorted_x_axis_elt = sorted(mutators_tab[mutator])

        for x_axis_elt in sorted_x_axis_elt:
            i = 0
            if x_axis_elt != init:
                i = int(x_axis_elt / gap)
            to_return += "({0},{1})".format(i, round(mutators_tab[mutator][x_axis_elt] * 10, 2))
            if x_axis_elt < limit:
                to_return += " -- "
            else:
                to_return += ";"
        to_return += "\n\n"

    return to_return

def main():
    convergence_file = sys.argv[1]
    path = sys.argv[1].rsplit('/')[0] + "/"
    project_name = ""

    f = open(convergence_file, 'r')

    current_conv = 1
    mutators_tab = init_mutators_tab()

    for l in f:
        project_line = l.split('&')
        if project_line[0] in projects:
            if project_name == "":
                project_name = project_line[0]
            actual_gap = int(project_line[3])
            if actual_gap > current_conv:

                #verification
                for mutator in mutators_tab:
                    if mutators_tab[mutator][current_conv] == -1:
                        if current_conv > gap:
                            #append the last element of the list is the informations are not available
                            mutators_tab[mutator][current_conv] = mutators_tab[mutator][current_conv - gap]
                        elif current_conv == gap:
                            mutators_tab[mutator][current_conv] = mutators_tab[mutator][1]
                        else:
                            mutators_tab[mutator][current_conv] = 0.0

                current_conv = actual_gap

            mutators_tab[project_line[4]][current_conv] = float(project_line[7])

    f.close()

    tikz_graph = transform_mutators_tab_into_graph(mutators_tab)

    path = "{0}{1}{2}{3}".format(path, "g_rslts_", project_name, ".tex")

    print(path)

    f = open(path, "w")
    f.write(tikz_graph)
    f.close()

    print("File closed!")

if __name__ == '__main__':
    main()
