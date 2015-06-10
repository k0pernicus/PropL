import sys
import os

from threading import Thread

#from libs.xml_lib import load_xml_document
from libs.xml_lib import is_valid_XML_documents
from libs.xml_lib import is_a_valid_XML_document
from libs.xml_lib import decompose_mutations

from libs.exceptions.NoArgument import NoArgument
from libs.exceptions.RunError import RunError

from libs.use_graph_lib import UseGraph

not_authorized_files = ['.DS_Store', '__init__.py']

def help():
    """
    Abstract: Print usage and functionalities of the program
    """

    return "\
    PropL program\n\
    ---------\n\
    ---------\n\
    \n\
    Usage\n\
    -----\n\
    \tprogram <path_of_file/directory> [--help|--debug]\n\
    \n\
    List of functionalities\n\
    -----------------------\n\
    \t--help: to print help - stop the program after printing\n\
    \t--debug: to enable the debugging mode (for developers)\n\
    "

def merge_smf_file(use_graph, doc, debug_mode = False):
    """
    Abstract: Function to merge the doc (given as 2nd parameter) with the usegraph object (given as 1st parameter)
    """

    #TODO: decompose the doc file with mutations elements -> computeLiaisons with these elements

    mutants_table = decompose_mutations(doc, debug_mode)

    for mutant in mutants_table:
        mutant_name, impacted_nodes = mutant
        use_graph.computeLiaisons(mutant_name, impacted_nodes)
        if debug_mode:
            print("mutant {0} with {1} impacted nodes".format(mutant_name, len(impacted_nodes)))

def main():

    if "--help" in sys.argv:
        print(help())
        sys.exit()

    if "--debug" in sys.argv:
        debug_mode = True
    else:
        debug_mode = False

    try:
        xml_doc = sys.argv[1]
    except Exception as excpt:
        raise NoArgument("Please to give at least the XML document (or repository) as argument...")

    #Verification of the path
    if os.path.exists(xml_doc):
        if os.path.isfile(xml_doc):
            #Transformation of the unique file -> list
            raise RunError("error : need a directory which contains 'run' and 'usegraph' files...")
        else:
            path = xml_doc
            xml_doc = os.listdir(path)

            #Absolute path for files
            for i in range(0, len(xml_doc)):
                xml_doc[i] = os.path.join(path, xml_doc[i])

            if debug_mode:
                print("{0} as directory".format(xml_doc))
                print("xml_doc : {0}".format(xml_doc))
    else:
        raise FailToLoad("Please to give an existing path for files...")

    #Verification of the XML validation
    print(is_valid_XML_documents(xml_doc))

    #analyse usegraph file
    usegraph_file = [file_name for file_name in xml_doc if "usegraph" in file_name]
    run_file = [file_name for file_name in xml_doc if "run" in file_name]

    if len(usegraph_file) == 0 or len(run_file) == 0:
        raise RunError("No use graph or run files in the specified directory...")

    #Creation of the use graph
    use_graph = UseGraph(i, usegraph_file[0], debug_mode)

    #Run
    use_graph.run()

    #Merge use graph and run
    merge_smf_file(use_graph, run_file[0], debug_mode)

if __name__ == '__main__':
    main()
